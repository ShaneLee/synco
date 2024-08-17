#!/usr/bin/env bash

chmod a+w $HOME/synco/photos
cd $HOME/synco
# docker build --target run-stage -t syncoserver .
docker-compose down
docker-compose up --build -d
cd -
# Start noddy logging
docker container logs -f synco_synco_1 >> logs/synco.log &
