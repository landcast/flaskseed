#!/bin/sh

nohup python run.py $@ > /dev/null 2>&1 &
sleep 1s
tail -f /var/log/flaskseed-debug.log
