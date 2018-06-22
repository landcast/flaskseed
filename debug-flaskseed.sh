#!/bin/sh

nohup python run.py $@ > /dev/null 2>&1 &
sleep 3s
tail -f /var/log/flaskseed-debug_`cat flaskseed.pid`.log
