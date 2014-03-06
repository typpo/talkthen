#!/bin/bash

echo "Running cron @ `date`"
pushd `dirname $0` >/dev/null
source venv/bin/activate
cd talkthen
./manage.py make_calls
popd >/dev/null
echo "Done."
