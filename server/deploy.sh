#!/usr/bin/env bash

chmod a+w $HOME/synco/photos
cd $HOME/synco

docker build --target run-stage -t syncoserver .

docker stop synco_synco_1 2>/dev/null || true
docker rm synco_synco_1 2>/dev/null || true

docker run -d --name synco_synco_1 -p 8000:8000 -v ~/synco:/app/data -e PYTHONPATH=/app/src syncoserver

cd -

echo "Successfully deployed synco server at $(date)" > logs/synco.log

nohup docker logs -f synco_synco_1 >> logs/synco.log 2>&1 &
