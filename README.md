# Space pictures telegram bot

This is bundle of scripts which can download space images from SpaceX and NASA via it's API and publish it on Telegram Channel.


## Requirements

 - python3.6+
 - `environs` library
 - `requests` library
 - `python-telegram-bot==13.0` library


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

Use taken information for fill settings in `.env` file. You can use `.env_example` as a template:
```
cp .env_example .env
vim .env
```

## How it works

Script uses three different sources for downloading space images and stores it in one folder. To prevent duplicates it uses SHA1. If there is no image in folder (all images was published), script will download another portion of images. **Note, image is removing from images folder after it'fs posting.**


## How to use

### Quick start

Fill `.env` file as shown above and run command:
```
python3 bot.py
```
And that's it! Bot will download images from sources and post one random image in your telegram channel.


### Arguments

You can also post your own image stored on your device, just set path to it location. The image will be posted immediately (and will not be removed):
```
python3 bot.py -f my_photos/cool_space_image.png
```

You can run infinity posting passing `-r` argument. In this case bot will post image every 4 hours with no ending from download folder:
```
python3 bot.py -r
```

To change hourly delay between posting, set `-d`:
```
python3 bot.py -d 2
```

Also you can change folder for downloaded images (default is `images`):
```
python3 bot.py -r -p downloaded_images
```

Here is example of infinity posting from `downloaded_images` folder with 1 hour delay:
```
python3 bot.py -r -p downloaded_images -d 1
```


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

### Use your own images with infinity posting

You can use any images you have or you found. Just copy it on `images` folder (or folder you changed from default). But note, **it will deleted after publication.**