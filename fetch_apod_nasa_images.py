import argparse
import os
import pathlib
import urllib.parse

from environs import Env
import requests

from downloader import download_img


env = Env()
env.read_env()


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download astronomy pictures of the day by NASA
        '''
    )
    parser.add_argument(
        '-c',
        '--count',
        default=10,
        type=int,
        help='Count of the images',
    )
    parser.add_argument(
        '-p',
        '--path',
        default='images',
        type=pathlib.Path,
        help='Path to folder to save images',
    )
    args = parser.parse_args()
    return args


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


def fetch_imgs_urls(url, count, api_key=env('NASA_API_KEY')):

    params = {
        'count': count,
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    imgs_urls = []
    for apod in response.json():
        if 'url' in apod and is_allowed_ext(apod['url']):
            imgs_urls.append(apod['url'])

    return imgs_urls


def main():
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    url = 'https://api.nasa.gov/planetary/apod'
    imgs_urls = fetch_imgs_urls(url, args.count)
    for img_url in imgs_urls:
        filename = extract_filename(img_url)
        filepath = os.path.join(args.path, filename)
        download_img(img_url, filepath)


if __name__ == '__main__':
    main()
