#!/bin/bash

echo "Running cron @ `date`"
source venv/bin/activate
cd talkthen
./manage.py make_calls
echo "Done."
