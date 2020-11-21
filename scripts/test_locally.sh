#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./.venv/bin/activate
source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    python3 ./server.py
fi

cd $start_pwd
