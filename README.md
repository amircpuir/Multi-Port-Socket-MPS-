
# 🛡️ Multi Port Socket (MPS)

A lightweight and high-performance native Python tunneling tool designed to forward multiple ports through a single TCP socket.

---

### 📥 Step 1: Download the Script
Copy and paste the following command into your terminal to download the script:

```bash
wget -O mps.py [https://raw.githubusercontent.com/amircpuir/Multi-Port-Socket-MPS-/main/mps.py](https://raw.githubusercontent.com/amircpuir/Multi-Port-Socket-MPS-/main/mps.py)
🚀 Step 2: Run in Screen (Background Mode)
To ensure the tunnel stays active after closing the terminal, run the script inside a screen session:

Bash
screen -S mps python3 mps.py
⚙️ Step 3: Configuration Guide
Once the script starts, follow these steps:

If you are on the Destination Server (Europe/Remote):

Select option 1.

Enter a tunnel port (e.g., 443).

If you are on the Bridge Server (Iran/Local):

Select option 2.

Enter your local app ports (e.g., 2091,8080).

Enter the Remote Server IP and the tunnel port you chose (443).

🔒 Step 4: Detach and Save (Crucial)
After the tunnel is established, to keep it running in the background:

Press and hold Ctrl, then press A.

Immediately press D.
The tunnel is now running safely in the background.

🛠 Useful Commands
Reconnect to session: screen -r mps

List active sessions: screen -ls

🆔 Official Channel: @Telhost1
