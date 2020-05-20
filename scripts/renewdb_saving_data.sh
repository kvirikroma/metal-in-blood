#!/bin/bash

if [[ $PWD == *"scripts"* ]]
then
    cd ..
fi

if [ -z ${PGPASSWORD+x} ]; then
    export PGPASSWORD
    echo "Enter the PostgreSQL password:"
    read -s PGPASSWORD
fi

pg_dump -Fc -Z0 --data-only -U api metalinblood > ./mibdb_data.pgdump

dropdb -U api metalinblood
createdb -U api metalinblood
psql metalinblood -U api < ./sql/mibdb.sql

pg_restore -U api --data-only -d metalinblood ./wkdb_data.pgdump
rm -f ./wkdb_data.pgdump
