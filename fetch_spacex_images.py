import argparse
import pathlib
import requests

from downloader import download_img


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Download images for SpaceX launches
        '''
    )
    parser.add_argument(
        '-i',
        '--id',
        help='SpaceX launch ID',
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


def fetch_urls_imgs(launch_url):

    response = requests.get(launch_url)
    response.raise_for_status()
    launch = response.json()

    imgs_urls = launch['links']['flickr']['original']

    return imgs_urls


def download_imgs(dirpath, launch_id='latest'):

    launch_url_template = 'https://api.spacexdata.com/v5/launches/{}'
    launch_url = launch_url_template.format(launch_id)
    imgs_urls = fetch_urls_imgs(launch_url)
    for img_url in imgs_urls:
        download_img(img_url, dirpath)


if __name__ == '__main__':
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    download_imgs(args.path, args.id)
