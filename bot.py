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

    args = parser.parse_args()
    return args


def run_bot(bot, dirpath, delay):

    while True:
        # if there is no unpublished images, let's download it
        if not os.listdir(dirpath):
            fetch_spacex_images.download_imgs(dirpath)
            fetch_apod_nasa_images.download_imgs(dirpath)
            fetch_epic_nasa_images.download_imgs(dirpath)

        random_filename = random.choice(os.listdir(dirpath))
        filepath = os.path.join(dirpath, random_filename)

        bot.send_photo(
            chat_id=env('TG_CHAT_ID'),
            photo=open(filepath, 'rb'),
        )

        os.remove(filepath)

        time.sleep(delay * 3600)  # hours to seconds


if __name__ == '__main__':
    args = read_args()

    pathlib.Path(args.path).mkdir(exist_ok=True)

    bot = telegram.Bot(token=env('TG_BOT_API_KEY'))
    run_bot(bot, args.path, args.delay)
