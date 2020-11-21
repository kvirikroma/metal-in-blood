#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    pg_dump -U mib_api --schema-only metalinblood > ./sql/mibdb.sql
    pg_dump -Fc -Z0 -U mib_api --data-only metalinblood > ./sql/data.pgdump
fi

cd $start_pwd
