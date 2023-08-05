import datetime
import os
import time

import backoff
import pendulum
import singer
import requests

from singer import logger, utils

CONFIG = {}
STATE = {}
LOGGER = logger.get_logger()
SESSION = requests.Session()

def get_abs_path(path):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def get_start():
    date = STATE.get('start_date', CONFIG['start_date'])

    return pendulum.parse(date).int_timestamp * 1000

def base_url():
    return "https://{0}.api.riotgames.com/lol".format(CONFIG['region'])

def default_headers():
    return {'X-Riot-Token': CONFIG['api_secret']}

@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      jitter=backoff.full_jitter,
                      max_tries=5)
def request(url, headers={}, query_params={}):
    url_headers = {**default_headers(), **headers}
    req = requests.Request("GET", url=url, headers=url_headers, params=query_params).prepare()

    LOGGER.info("GET {}".format(req.url))
    resp = SESSION.send(req)

    if resp.status_code == 429:
        retry_after = resp.headers.get('Retry-After')
        if retry_after:
            LOGGER.info("Sleeping for {} seconds due to rate limiting".format(retry_after))
            time.sleep(int(retry_after))

            return request(url, headers)

    if resp.status_code >= 400:
        resp.raise_for_status()

    return resp.json()

def get_name():
    return CONFIG['summoner_name'].lower()

def get_account_id():
    name = get_name()
    url = base_url() + "/summoner/v3/summoners/by-name/{}".format(name)

    return request(url)['accountId']

def get_match_ids(account_id):
    url = base_url() + "/match/v3/matchlists/by-account/{}".format(account_id)
    query_params = {
        'beginTime': get_start(),
        'queue': CONFIG['queue'],
        'season': CONFIG['season']
    }
    resp = request(url, query_params=query_params)

    return resp.get('matches', [])

def get_self_id(participantIdentities):
    name = get_name()
    self = [self for self in participantIdentities if self['player']['summonerName'].lower() == name]

    return self[0]['participantId']

def get_match(account_id, match_id):
    url = base_url() + "/match/v3/matches/{}".format(match_id['gameId'])
    match = request(url)

    match['id'] = account_id

    participants = match.pop('participants', None)
    teams = match.pop('teams', None)

    self_id = get_self_id(match['participantIdentities'])
    self_stats = [stats for stats in participants if stats['participantId'] == self_id]
    self_lane = self_stats[0]['timeline']['lane']
    self_team_id = self_stats[0]['teamId']
    self_team = [t for t in teams if t['teamId'] == self_team_id]

    # mid lane can be represented as either of these in the api
    if self_lane in ['MID', 'MIDDLE']:
        opponent_stats = [stats for stats in participants if stats['participantId'] != self_id and stats['timeline']['lane'] in ['MID', 'MIDDLE']]
    else:
        opponent_stats = [stats for stats in participants if stats['participantId'] != self_id and stats['timeline']['lane'] == self_lane]
    opponent_team = [t for t in teams if t['teamId'] != self_team_id]

    match['self_stats'] = self_stats[0]
    match['self_team'] = self_team[0]
    match['opponent_team'] = opponent_team[0]
    # there's cases when the api won't know who your opponent was
    match['opponent_stats'] = opponent_stats[0] if len(opponent_stats) > 0 else None

    updated_date = datetime.datetime.fromtimestamp(match['gameCreation'] * 0.001)
    utils.update_state(STATE, 'start_date', updated_date.strftime('%Y-%m-%d'))

    singer.write_record('matches', match)

def replicate():
    start_date = STATE.get('start_date', CONFIG['start_date'])
    LOGGER.info("Using start date of {}".format(start_date))

    account_id = get_account_id()
    match_ids = get_match_ids(account_id)

    LOGGER.info("Starting sync")

    if match_ids:
        matches_json = get_abs_path('schemas/matches.json')
        matches_schema = utils.load_json(matches_json)
        singer.write_schema('matches', matches_schema, ['id', 'gameId'])

    LOGGER.info("Replicating {} matches".format(len(match_ids)))

    for match_id in match_ids:
        get_match(account_id, match_id)

    LOGGER.info("Replicated {} matches".format(len(match_ids)))

    # match ids are not ordered by time so we cannot incrementally write STATE records
    if match_ids:
        singer.write_state(STATE)

    LOGGER.info("Sync completed")

def main():
    required_keys = ['summoner_name', 'region', 'api_secret', 'start_date', 'queue', 'season']
    args = utils.parse_args(required_keys)

    CONFIG.update(args.config)
    STATE.update(args.state)

    replicate()

if __name__ == '__main__':
    main()
