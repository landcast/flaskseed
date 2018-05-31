#!/bin/sh

export eip=`curl ipecho.net/plain`
./debug-ustutor.sh -E $eip
