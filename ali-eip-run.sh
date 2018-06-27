#!/bin/sh
rm ./flaskseed.pid -rf
export eip=`curl -s ipecho.net/plain`
./debug-flaskseed.sh -E $eip
