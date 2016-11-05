#!/bin/sh

# call via cron:
# $ crontab -e
# @reboot /path/to/runscope.sh

cd /home/pi/cinemascope
./tkscope.py spasm_v7_800.mp4
