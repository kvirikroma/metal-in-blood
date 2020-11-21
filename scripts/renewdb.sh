#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    dropdb -U mib_api metalinblood
    createdb -U mib_api metalinblood
    psql metalinblood -U mib_api < ./sql/mibdb.sql
    pg_restore -U mib_api --data-only -d metalinblood ./sql/data.pgdump
fi

cd $start_pwd
