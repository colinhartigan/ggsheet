import requests
from os import listdir
from os.path import isfile, join
import sys

from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

def fetch_images(data_type:str)->None:
    url={}
    if data_type == 'agent':
        response = requests.get('https://playvalorant.com/page-data/en-us/agents/page-data.json')
        for _ in response.json()['result']['data']['allContentstackAgentList']['nodes'][0]['agent_list']:
            url[_['related_content'][0]['title'].lower().replace('/', '')] = _['agent_image']['url']
    elif data_type == 'map':
        response = requests.get('https://valorant-api.com/v1/maps')
        for _ in response.json()['data']:
            url[_['displayName'].lower()] = _['splash']
        del url['the range']

    path = f'.\\data\\{data_type}s'
    old = [_.replace('agent_', '').replace('map_', '').replace('.png', '') for _ in [f for f in listdir(path) if isfile(join(path, f))]]
    new = list(set(url.keys()) - set(old))
    if new:
        download(new, data_type, path, url)
    else:
        sys.stdout.write(f'No new {data_type} image need to be downloaded\r')
        sys.stdout.flush()


def download(new:list, data_type:str, path:str, url:dict)->None:
    for i, _ in enumerate(new):
        progress(i, len(new), suffix=f' Downloading new {data_type} image: {_}')
        response = requests.get(url[_], timeout=30)
        with open(f'{path}\\{data_type}_{_}.png', 'wb') as f:
            f.write(response.content)

def fetch_matches(mgr, content) -> list:
    matches = mgr.client.fetch_match_history()["History"]
    choices = [Choice("custom", "use my own match id"), Separator()]
    for i, match in enumerate(matches):
        match_data = mgr.client.fetch_match_details(match["MatchID"])

        me = next(player for player in match_data["players"] if player["subject"] == mgr.client.puuid)
        my_team = next(team for team in match_data["teams"] if team["teamId"] == me["teamId"])
        other_team = next(team for team in match_data["teams"] if team["teamId"] != me["teamId"])

        queue = match_data["matchInfo"]["queueID"]
        if queue == " " or queue == "":
            queue = "custom"
        match_id = match_data["matchInfo"]["matchId"]
        score = f"{my_team['roundsWon']}-{other_team['roundsWon']}"

        agent = next(agent for agent in content["agents"] if agent["uuid"] == me["characterId"])
        agent = agent["display_name"]

        string = f"[{score}] {queue} - {agent} ({match_id})"
        choices.append(Choice(match_id, string))

        progress(i, len(matches), suffix=f' Fetching recent matches')
    return choices


def progress(count, total, suffix=''):
    bar_len = 20
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percents, '%', suffix + ' '*20))
    sys.stdout.flush()

if __name__ == '__main__':
    fetch_images('agent')
    fetch_images('map')
