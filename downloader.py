import hashlib
import os
import requests
import urllib.parse


IMG_MAX_SIZE = 20971520  # 20Mb


def download_img(url, dirpath, api_key=None):

    headers = {
        'User-Agent': 'Curl'
    }

    params = {}
    if api_key:
        params['api_key'] = api_key

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    file_hash = hashlib.sha1(response.content).hexdigest()
    file_ext = fetch_img_ext(url)
    filename = f'{file_hash}.{file_ext}'

    if all([
        not is_downloaded(file_hash, dirpath),
        file_ext in ('jpg', 'jpeg', 'gif', 'png'),
        len(response.content) < IMG_MAX_SIZE
    ]):
        filepath = os.path.join(dirpath, filename)
        with open(filepath, 'wb') as file:
            file.write(response.content)


def is_downloaded(file_hash, dirpath):

    downloaded_filenames = os.listdir(dirpath)
    downloaded_img_hashes = []
    for filename in downloaded_filenames:
        downloaded_img_hashes.append(filename.split('.')[0])

    return file_hash in downloaded_img_hashes


def fetch_img_ext(url):
    img_path_in_url = urllib.parse.urlsplit(url).path
    _, img_ext = os.path.splitext(img_path_in_url)
    return img_ext[1:]
