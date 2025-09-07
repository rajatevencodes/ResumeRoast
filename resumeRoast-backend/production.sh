#!/bin/sh

# Start the web server in the background using '&'
python server.py &

# Start the RQ worker in the foreground
# This keeps the container running
rq worker --with-scheduler --url redis://valkey:6379