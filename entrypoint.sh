#!/bin/sh
flask db migrate
flask db upgrade
flask run --host=0.0.0.0
# exec gunicorn -b :5000 \
#     --name revolut_api \
#     --access-logfile - \
#     --error-logfile - \
#     run:app
