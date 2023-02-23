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

## How to use


