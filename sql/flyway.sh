#!/bin/bash
# script to run migrations

if [ $# -eq 0 ]; then
    echo "please provide flyway command ex: migrate, clean"
    echo "see https://flywaydb.org/documentation/usage/commandline/"
    exit
else
    # get the db admin user/pwd
    read -ep " username: " USER_NAME
    read -ep " password: " PWD

    # get absolute path to sql scripts
    MIGRATE_PATH=$(realpath ./scripts)

    bash -c "flyway $1 -user=$USER_NAME -password=$PWD -url=jdbc:mariadb://localhost -schemas=SkyWeather2 -locations=filesystem:$MIGRATE_PATH"
fi

