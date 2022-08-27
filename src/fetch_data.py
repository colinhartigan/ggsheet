import requests
from os import listdir
from os.path import isfile, join

def fetch(data_type:str)->None:
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
        download(new, data_type ,path, url)
    else:
        print(f'No new {data_type} image need to be downloaded')

def download(new:list, data_type:str, path:str, url:dict)->None:
    for _ in new:
        print(f'Downloading new {data_type} image: {_}, url: {url[_]}')
        response = requests.get(url[_], timeout=30)
        with open(f'{path}\\{data_type}_{_}.png', 'wb') as f:
            f.write(response.content)

def fetch_all()-> None:
    fetch('agent')
    fetch('map')

if __name__ == '__main__':
    fetch_all()