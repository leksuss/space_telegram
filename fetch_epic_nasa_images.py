import argparse
import os
import pathlib
from datetime import datetime

from environs import Env
import requests

from downloader import download_img


env = Env()
env.read_env()


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download Earth polychromatic imaging camera by NASA
        '''
    )
    parser.add_argument(
        '-d',
        '--date',
        default=datetime.today().strftime('%Y-%m-%d'),
        type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
        help='Date of taking a photo, format yyyy-mm-dd',
    )
    parser.add_argument(
        '-p',
        '--path',
        default='epic_images',
        type=pathlib.Path,
        help='Path to folder to save images',
    )
    args = parser.parse_args()
    return args


def fetch_imgs_names(url, api_key=env('API_KEY')):

    params = {
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return (epic_image['image'] for epic_image in response.json())


def generate_img_url(date, image_name):

    url_pattern = 'https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png' # noqa
    return url_pattern.format(
        date.year,
        date.strftime('%m'),
        date.strftime('%d'),
        image_name,
    )


def main():
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    url = 'https://api.nasa.gov/EPIC/api/natural/{}'.format(
        args.date.strftime("%Y-%m-%d"),
    )

    imgs_names = fetch_imgs_names(url)
    for img_name in imgs_names:
        img_url = generate_img_url(args.date, img_name)
        filepath = os.path.join(args.path, f'{img_name}.png')
        download_img(img_url, filepath, env('API_KEY'))


if __name__ == '__main__':
    main()
