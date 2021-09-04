#!/usr/bin/bash

source /home/pi/python/fastapi/bin/activate
cd /home/pi/fastapi
uvicorn main:app --reload --host 192.168.20.200 --port 8000
