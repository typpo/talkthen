#!/bin/bash -e
source venv/bin/activate
gunicorn -b 127.0.0.1:3333 --pythonpath srv srv.wsgi -D
