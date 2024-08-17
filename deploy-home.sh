#!/usr/bin/env bash

source ~/.bin/dotfiles/.secrets.zconfig

scp -r Dockerfile .dockerignore docker-compose.yml shane@$NIGHTINGALE:~/synco/
rsync -av --delete server/ shane@$NIGHTINGALE:~/synco/server/
ssh shane@$NIGHTINGALE "~/synco/server/deploy.sh"
