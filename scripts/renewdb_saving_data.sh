#!/bin/bash

export start_pwd=$PWD
while [[ $PWD == *"scripts"* ]]; do
    cd ..
done

source ./scripts/auxiliary/prepare_launch.sh

if $(password_check); then
    pg_dump -Fc -Z0 --data-only -U mib_api metalinblood > ./mibdb_data.pgdump

    dropdb -U mib_api metalinblood
    createdb -U mib_api metalinblood
    psql metalinblood -U mib_api < ./sql/mibdb.sql

    pg_restore -U mib_api --data-only -d metalinblood ./sql/wkdb_data.pgdump
    rm -f ./wkdb_data.pgdump
fi

cd $start_pwd
