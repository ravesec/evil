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
nft add chain venom input \{ type filter hook input priority -101 \; policy continue\; \}
nft add chain venom output \{ type filter hook output priority -101 \; policy continue\; \}
nft add rule venom input tcp dport { 7983 } accept
nft add rule venom output tcp sport { 7983 } accept