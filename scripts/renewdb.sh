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

dropdb -U api metalinblood
createdb -U api metalinblood
psql metalinblood -U api < ./sql/mibdb.sql
pg_restore -U api --data-only -d metalinblood ./sql/data.pgdump
