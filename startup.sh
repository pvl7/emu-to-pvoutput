#!/usr/bin/env bash
#
# Author: "Pavel Lu", (c) 2020
# License: "GPL"
# Version: "0.1"
# Contact: email@pavel.lu

# start loop and poll the device every 5 min
while true ; do 
  python3 rainforest-to-pvoutput.py
  if [ $? -eq 3 ] ; then
    echo "Fatal error, exiting."
    exit 1
  fi

  # wait 4 min
  sleep 240
done
