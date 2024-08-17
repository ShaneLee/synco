#!/usr/bin/env bash

chmod a+w $HOME/synco/photos
cd $HOME/synco
# docker build --target run-stage -t syncoserver .
docker-compose down
docker-compose up --build -d
cd -
# Overwrite sorg log file on deploy
 echo "Successfully deployed synco server at $(date)" > logs/synco.log
# Start noddy logging
nohup docker container logs -f synco_synco_1 >> logs/synco.log 2>&1 &
