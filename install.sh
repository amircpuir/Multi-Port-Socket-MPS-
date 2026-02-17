cat << 'EOF' > install.sh
#!/bin/bash

sudo apt update && sudo apt install screen wget -y


wget -O mps.py https://raw.githubusercontent.com/amircpuir/Multi-Port-Socket-MPS-/main/mps.py


echo -e "\033[92m[+] Installation Complete!\033[0m"
echo -e "\033[93m[!] Starting MPS in a new Screen session...\033[0m"
sleep 2

screen -S mps_tunnel python3 mps.py

EOF

chmod +x install.sh
