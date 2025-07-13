#!/bin/bash
mkdir -p collected_data

echo "[*] Collecting important config files..."

cp /etc/ssh/sshd_config collected_data/ 2>/dev/null
cp /etc/nginx/nginx.conf collected_data/ 2>/dev/null
cp /etc/apache2/apache2.conf collected_data/ 2>/dev/null
crontab -l > collected_data/user_crontab.txt 2>/dev/null
cat /etc/crontab > collected_data/system_crontab.txt 2>/dev/null

echo "[+] Config files collected."
