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

if
    export JWT_KEY=$(ccrypt -d ./scripts/encrypted_vars/jwt.cpt -c -K "$PGPASSWORD")
then
    if [[ $JWT_KEY == '' ]]; then
        echo "Incorrect password"
        exit
    fi
else
    echo "Something went wrong"
    exit
fi
