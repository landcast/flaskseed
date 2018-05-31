#!/bin/sh

export eip=`curl -s ipecho.net/plain`
./debug-ustutor.sh -E $eip
