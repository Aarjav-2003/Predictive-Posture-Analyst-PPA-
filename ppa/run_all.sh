#!/bin/bash
echo "=== Starting Predictive Posture Analyst Data Collection ==="

chmod +x collect_*.sh

./collect_network.sh
./collect_users.sh
./collect_processes.sh
./collect_services.sh
./collect_configs.sh

echo "=== Collection Complete. Data stored in 'collected_data/' ==="
