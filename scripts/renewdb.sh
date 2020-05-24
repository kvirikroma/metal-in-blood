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

dropdb -U mib_api metalinblood
createdb -U mib_api metalinblood
psql metalinblood -U mib_api < ./sql/mibdb.sql
pg_restore -U mib_api --data-only -d metalinblood ./sql/data.pgdump
