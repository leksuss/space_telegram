import os
import requests
import urllib.parse


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


def extract_filename(url):
    img_path_in_url = urllib.parse.urlsplit(url).path
    return os.path.basename(img_path_in_url)


def fetch_img_ext(url):
    img_path_in_url = urllib.parse.urlsplit(url).path
    _, img_ext = os.path.splitext(img_path_in_url)
    return img_ext[1:]


def is_allowed_ext(url):
    ext = fetch_img_ext(url)
    allowed_ext = 'jpg', 'jpeg', 'gif', 'png'
    return ext in allowed_ext
