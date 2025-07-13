#!/bin/bash
mkdir -p collected_data

echo "[*] Collecting service info..."

systemctl list-units --type=service --all > collected_data/system_services.txt
service --status-all > collected_data/service_status_all.txt 2>/dev/null

echo "[+] Service info collected."
