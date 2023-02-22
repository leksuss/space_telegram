import argparse
import os
import pathlib

from environs import Env
import requests

import utils

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
        default='apod_images',
        type=pathlib.Path,
        help='Path to folder to save images',
    )
    args = parser.parse_args()
    return args


def fetch_imgs_urls(url, count, api_key=env('API_KEY')):

    params = {
        'count': count,
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    imgs_urls = []
    for apod in response.json():
        if 'url' in apod and utils.is_allowed_ext(apod['url']):
            imgs_urls.append(apod['url'])

    return imgs_urls


if __name__ == '__main__':
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    url = 'https://api.nasa.gov/planetary/apod'
    imgs_urls = fetch_imgs_urls(url, args.count)
    for img_url in imgs_urls:
        filename = utils.extract_filename(img_url)
        filepath = os.path.join(args.path, filename)
        utils.download_img(img_url, filepath)
