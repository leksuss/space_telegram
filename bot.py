import argparse
import os
import pathlib
import random
import time

from environs import Env
import telegram

import fetch_spacex_images
import fetch_apod_nasa_images
import fetch_epic_nasa_images


DELAY_BETWEEN_PUBLISHES_IN_HOURS = 4

env = Env()
env.read_env()


def read_args():
    parser = argparse.ArgumentParser(
        description='''
            Publish images to telegram channel
            given from SpaceX and NASA APIs
        '''
    )
    parser.add_argument(
        '-f',
        '--filepath',
        required=False,
        type=str,
        help='Path to file for manual posting just once',
    )
    parser.add_argument(
        '-d',
        '--delay',
        default=DELAY_BETWEEN_PUBLISHES_IN_HOURS,
        type=int,
        help='Period between two publishes, in hours',
    )
    parser.add_argument(
        '-p',
        '--path',
        default='images',
        type=pathlib.Path,
        help='Path to folder to save downloaded images',
    )
    parser.add_argument(
        '-r',
        '--infinity_run',
        action='store_true',
        help='Set infinity posting mode',
    )
    args = parser.parse_args()
    return args


def post_random_image(bot, dirpath):

    download_images_if_needed(dirpath)

    random_filename = random.choice(os.listdir(dirpath))
    filepath = os.path.join(dirpath, random_filename)

    post_image(bot, filepath)

    return filepath


def post_image(bot, filepath):

    bot.send_photo(
        chat_id=env('TG_CHAT_ID'),
        photo=open(filepath, 'rb'),
    )


def download_images_if_needed(dirpath):

    if not os.listdir(dirpath):
        fetch_spacex_images.download_imgs(dirpath)
        fetch_apod_nasa_images.download_imgs(dirpath)
        fetch_epic_nasa_images.download_imgs(dirpath)


def run_infinity_posting(bot, dirpath, delay):

    while True:
        download_images_if_needed(dirpath)
        posted_filepath = post_random_image(bot, dirpath)

        os.remove(posted_filepath)

        time.sleep(delay * 3600)  # hours to seconds


if __name__ == '__main__':
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    bot = telegram.Bot(token=env('TG_BOT_API_KEY'))

    if args.filepath:
        post_image(bot, args.filepath)
    elif args.infinity_run:
        run_infinity_posting(bot, args.path, args.delay)
    else:
        posted_filepath = post_random_image(bot, args.path)
        os.remove(posted_filepath)
