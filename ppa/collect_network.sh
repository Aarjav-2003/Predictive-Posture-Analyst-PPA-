#!/bin/bash
mkdir -p collected_data

echo "[*] Collecting network info..."

ip a > collected_data/network_interfaces.txt
ss -tulnp > collected_data/open_ports.txt
iptables-save > collected_data/iptables_rules.txt 2>/dev/null
ufw status verbose > collected_data/ufw_status.txt 2>/dev/null

echo "[+] Network info collected."
