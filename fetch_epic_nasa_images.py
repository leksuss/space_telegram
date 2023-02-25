import argparse
import pathlib
from datetime import datetime

from environs import Env
import requests

from downloader import download_img


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download Earth polychromatic imaging camera by NASA
        '''
    )
    parser.add_argument(
        '-d',
        '--date',
        type=lambda d: datetime.strptime(d, '%Y-%m-%d').date(),
        help='Date of taking a photo, format yyyy-mm-dd',
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


def fetch_imgs_names_and_date(url, api_key):

    params = {
        'api_key': api_key,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    epic_images = response.json()

    imgs_names = tuple(epic_image['image'] for epic_image in epic_images)
    latest_date = datetime.strptime(
        epic_images[0]['date'],
        '%Y-%m-%d %H:%M:%S'
    ).date()

    return imgs_names, latest_date


def generate_img_url(date, image_name):

    url_pattern = 'https://api.nasa.gov/EPIC/archive/natural/{}/{}/{}/png/{}.png' # noqa
    return url_pattern.format(
        date.year,
        date.strftime('%m'),
        date.strftime('%d'),
        image_name,
    )


def download_imgs(api_key, dirpath, setted_date=None):

    url = 'https://api.nasa.gov/EPIC/api/natural'
    if setted_date:
        url += f'/date/{setted_date.strftime("%Y-%m-%d")}'

    imgs_names, latest_date = fetch_imgs_names_and_date(url)

    for img_name in imgs_names:
        img_url = generate_img_url(setted_date or latest_date, img_name)
        download_img(img_url, dirpath, api_key)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env('NASA_API_KEY')

    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    download_imgs(api_key, args.path, args.date)
