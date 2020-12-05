#!/bin/bash

if [[ $PWD == *"scripts"* ]]
then
    cd ..
fi

source ./scripts/auxiliary/prepare_launch.sh

git pull origin master

docker-compose build mib-api
docker-compose up -d mib-api
