#!/usr/bin/env bash
#
# Author: "Pavel Lu", (c) 2020
# License: "GPL"
# Version: "0.2"
# Contact: email@pavel.lu

# start loop and poll the device every 5 min
while true ; do 
  /usr/bin/env python3 /opt/emu-to-pvoutput/rainforest-to-pvoutput.py
  if [ $? -eq 3 ] ; then
    echo "Fatal error, exiting."
    exit 1
  fi

  # wait 4 min
  sleep 240
done
