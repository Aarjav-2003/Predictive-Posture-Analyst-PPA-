#!/bin/bash
mkdir -p collected_data

echo "[*] Collecting user info..."

who > collected_data/logged_in_users.txt
last -n 20 > collected_data/last_logins.txt
cat /etc/passwd > collected_data/passwd_file.txt
cat /etc/group > collected_data/group_file.txt
passwd -S $(cut -d: -f1 /etc/passwd) > collected_data/password_status.txt 2>/dev/null
sudo -l -U $(whoami) > collected_data/sudo_privileges.txt 2>/dev/null

echo "[+] User info collected."
