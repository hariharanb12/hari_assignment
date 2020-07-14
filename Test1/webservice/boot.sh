#!/bin/sh
source venv/bin/activate
gunicorn --certfile=certs/server.crt --keyfile=certs/server.key -b :5000 flasky:app
