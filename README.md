# telegram-filter
Filter telegram


## Create the environment first (mac)
* source <path to conda>/bin/activate
* conda init
* conda create --name telegram
* conda activate telegram

## Install telethon
* pip3 install telethon

## Create Telegram app
* https://my.telegram.org/apps This websiste will guide you.
* Copy and save app id and hash.
* Create an new channel where you want to publish the details. ( You can mute other group randing :))

### Run
* Activate conda env
* python telegram_reader.py

### Important file
* Rename credential.template.json to credential.json and fill the values with your API values.
* 

