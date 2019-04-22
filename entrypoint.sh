#!/bin/sh
flask db migrate
flask db upgrade
flask initdb
flask run --host=0.0.0.0
