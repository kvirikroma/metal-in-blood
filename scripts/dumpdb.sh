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

pg_dump -U mib_api --schema-only metalinblood > ./sql/mibdb.sql

pg_dump -Fc -Z0 -U mib_api --data-only metalinblood > ./sql/data.pgdump
