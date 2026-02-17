#!/bin/bash

sudo apt update && sudo apt install screen wget -y

wget -O mps.py https://raw.githubusercontent.com/amircpuir/Multi-Port-Socket-MPS-/main/mps.py

echo -e "\033[92m[+] Installation Complete!\033[0m"
echo -e "\033[93m[!] Starting MPS inside Screen session 'mps_tunnel'...\033[0m"
sleep 2

screen -dmS mps_tunnel python3 mps.py
screen -r mps_tunnel
