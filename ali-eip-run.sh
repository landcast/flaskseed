#!/bin/sh

export eip=`curl -s ipecho.net/plain`
./debug-flaskseed.sh -E $eip
