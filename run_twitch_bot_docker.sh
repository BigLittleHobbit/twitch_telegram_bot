#!/bin/bash

docker run -it --name twitch_bot -v $(pwd):/home/user twitch_telegram_bot:v0.2
