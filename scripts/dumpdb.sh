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

pg_dump -U api --schema-only metalinblood > ./sql/mibdb.sql

pg_dump -Fc -Z0 -U api --data-only metalinblood | pxz -c -6 -T12 > ./sql/data.pgdump.xz
