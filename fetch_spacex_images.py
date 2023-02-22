import argparse
import os
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
        default='spacex_images',
        type=pathlib.Path,
        help='Path to folder to save images',
    )
    args = parser.parse_args()
    return args


def fetch_launch_imgs(launch_url, imgs_folder):

    response = requests.get(launch_url)
    response.raise_for_status()
    launch = response.json()

    imgs_urls = launch['links']['flickr']['original']

    for i, img_url in enumerate(imgs_urls):
        filepath = os.path.join(imgs_folder, f'space_{i}.jpg')
        download_img(img_url, filepath)


def main():
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    launch_url_template = 'https://api.spacexdata.com/v5/launches/{}'
    launch_url = launch_url_template.format(args.id if args.id else 'latest')
    fetch_launch_imgs(launch_url, args.path)


if __name__ == '__main__':
    main()
