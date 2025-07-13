#!/bin/bash
mkdir -p collected_data

echo "[*] Collecting process info..."

ps aux > collected_data/running_processes.txt
lsmod > collected_data/kernel_modules.txt

echo "[+] Process info collected."
