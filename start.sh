#!/bin/sh
set -e

# Start uvicorn in background on port 8001
uvicorn kjvstudy_org.server:app --host 127.0.0.1 --port 8001 &

# Wait for uvicorn to be ready
sleep 2

# Start nginx in foreground on port 8000
exec nginx -g 'daemon off;'
