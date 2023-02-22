import os
import requests


def download_img(url, filepath, api_key=None):

    headers = {
        'User-Agent': 'Curl'
    }

    params = {}
    if api_key:
        params['api_key'] = api_key

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    with open(filepath, 'wb') as file:
        file.write(response.content)

    return bool(os.path.getsize(filepath))
