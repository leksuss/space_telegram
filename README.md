# Space pictures telegram bot

This is bundle of scripts which can download space images from SpaceX and NASA via it's API and publish it on Telegram Channel.


## Requirements

 - python3.6+
 - `environs` library
 - `requests` library
 - `python-telegram-bot` library


## How to install

Get the source code of this repo:
```
git clone https://github.com/leksuss/space_telegram.git
```

Open project folder:
```
cd space_telegram
```

Then install dependencies:
```
# If you would like to install dependencies inside virtual environment, you should create it first.
pip3 install -r requirements.txt
```

## How to setup

This app uses NASA API and requires it's `API_KEY`. Just go [here](https://api.nasa.gov/) and fill simple form.

Also you should made some things with telegram:
 - [create telegram bot](https://core.telegram.org/bots#how-do-i-create-a-bot), receive token
 - create telegram channel (or use existing) and get it's username (it looks like `@username`).

Use taken information for fill settings in `.env` file. You can use `.env_example` as template:
```
cp .env_example .env
vim .env
```

## How it works

Script uses three different sources for downloading space images and stores it in one folder. To prevent duplicates it uses SHA1. **Note, image removed after it's posting.** If there is no image in folder (all images was published), script is downloading another portion of images.


## How to use

### Quick start

Fill `.env` file as shown above and run command:
```
python3 bot.py
```
And that's it! Bot will post one image every 4 hour at your telegram channel.


### Arguments

You can also set delay in hours between posting, default value is 4:
```
python3 bot.py --delay 2
```
And a folder for downloaded images, default value is `images`:
```
python3 bot.py --path downloaded_images
```
Of course you can combine it. And both of them is optional.


### Using scripts for download images

You can manually run each of three scripts to download images with different params. By deffault all scripts download images to `images` folder. You can change it with `--path` argument.

1. `fetch_spacex_images.py` downloads latest SpaceX launch images by default. You can get another images by setting `--id` argument as launch id taken from [list of launches](https://api.spacexdata.com/v5/launches):
```
python3 fetch_spacex_images.py --id=5eb87cecffd86e000604b33f
```

2. `fetch_epic_nasa_images.py` downloads latest Eath images by default. You can get another images by setting `--date` argument. But note, NASA return images at least two days before today. You can't receive Eath images for today and yesterday. Date format is important:
```
python3 fetch_epic_nasa_images.py --date=yyyy-mm-dd
```

3. `fetch_apod_nasa_images.py` downloads astronomy images of the day. By default it download 10 images. You can changit via `--count` argument:
```
python3 fetch_spacex_images.py --count=20
```

### Use your own images

You can use any images you have or you found. Just upload it on `images` folder (or folder you changed from default). But note, **it will deleted after publication.**