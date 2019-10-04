#!/usr/bin/env bash
export LC_ALL="en_US.UTF-8"
export LC_CTYPE="en_US.UTF-8"
export FLASK_APP=medmap
export FLASK_ENV=development
if [ -e 'instance/medmap.sqlite' ]; then
    echo "Database already exists."
    echo "Press n/N to drop existing table, any other key to use existing database."
    read ch
    if  [ "$ch" = "N" ] || [ "$ch" = "n" ]; then
        echo Initializing the database
        flask init-db
    fi
fi
flask run
