#!/usr/bin/env bash

set -e

docker build --target test-stage -t synco-tests .
docker run synco-tests
