#!/bin/bash

if [ ! -f ./migrations ]; then
    echo "db not created yet... creating..."
    python3 run.py db init && python3 run.py db migrate && python3 run.py db upgrade
else
    python3 run.py db migrate && python3 run.py db upgrade
fi

python3 run.py runserver