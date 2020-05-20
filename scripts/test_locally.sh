#!/bin/bash

if [[ $PWD == *"scripts"* ]]
then
    cd ..
fi

source ./.venv/bin/activate
source ./scripts/auxiliary/prepare_launch.sh

python3 ./server.py
