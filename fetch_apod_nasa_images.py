import argparse
import pathlib

from environs import Env
import requests

from downloader import download_img


COUNT_DOWNLOADED_IMGS = 10


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download astronomy pictures of the day by NASA
        '''
    )
    parser.add_argument(
        '-c',
        '--count',
        default=COUNT_DOWNLOADED_IMGS,
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


def fetch_imgs_urls(api_key, url, count):

    params = {
        'count': count,
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    apod_imgs = response.json()

    imgs_urls = [img['url'] for img in apod_imgs if 'url' in img]

    return imgs_urls


def download_imgs(api_key, dirpath, count=COUNT_DOWNLOADED_IMGS):

    url = 'https://api.nasa.gov/planetary/apod'
    imgs_urls = fetch_imgs_urls(api_key, url, count)
    for img_url in imgs_urls:
        download_img(img_url, dirpath, api_key)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env('NASA_API_KEY')

    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    download_imgs(api_key, args.path, args.count)
