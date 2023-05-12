import pickle
import os
import time

# Get sing-box v1.3 beta11 and place it in root
print('--------> Downloading sing-box\n\n')
if not os.path.exists('/root/sing-box'):
    os.system('curl -Lo /root/sb https://github.com/SagerNet/sing-box/releases/download/v1.3-beta11/sing-box-1.3-beta11-linux-amd64.tar.gz && tar -xzf /root/sb && cp -f /root/sing-box-*/sing-box /root && rm -r /root/sb /root/sing-box-* && chown root:root /root/sing-box && chmod +x /root/sing-box')
    print('--------Downloading sing-box finished--------\n\n')
    sing_box_new = True
else:
    print('--------sing-box Already exists--------\n\n')
    sing_box_new = False


# Create user_data.pkl for the bot
print('--------> Creating user_data\n\n')
user_data = {
    "chat_id":"",
    "user_id":"",
    "channel_id": "",
    "server_IP": "",
    "listen_port": 443,
    "bot_token": "",
    "renewal_interval":3600
}
user_data["chat_id"] = input("\nYou want the bot to send messages to channel or you?\n----> Type  me or ch: ")
while not user_data["chat_id"] in ('me', 'ch'):
    user_data["chat_id"] = input("\n----> Please type  me or ch: ")
user_data["server_IP"] = input("Enter server IP: ")
user_data["listen_port"] = int(input("Enter port number: "))
user_data["channel_id"] = input("Enter channel ID you got from @myidbot: ")
user_data["bot_token"] = input("Enter bot token: ")
user_data["renewal_interval"] = int(input("Enter renewal interval in seconds: "))

with open("/root/user_data.pkl", "wb") as f:
    pickle.dump(user_data, f)
    print(f"-------user_data was created!-------\n{user_data}\n\n")

print('--------> Downloading configer.py\n\n')
os.system('curl -Lo /root/configer.py https://raw.githubusercontent.com/hrostami/sb-server-configer/master/configer.py')
os.system('pip install python-telegram-bot==13.5')
time.sleep(1)
print('--------> Setting up Services \n\n')
if sing_box_new:
    os.system('curl -Lo /etc/systemd/system/sing-box.service https://raw.githubusercontent.com/iSegaro/Sing-Box/main/sing-box.service')
time.sleep(1)
if not os.path.exists('/etc/systemd/system/configer.service'):
    os.system('curl -Lo /etc/systemd/system/configer.service https://raw.githubusercontent.com/hrostami/sb-server-configer/master/configer.service')
    os.system('systemctl daemon-reload')
    os.system('sleep 0.2')
    os.system('systemctl enable configer.service')
    os.system('sleep 0.2')
    os.system('systemctl start configer.service')
else:
    os.system('systemctl restart configer.service')
print('--------Setting up Services finished --------\n\n')
print('-------->  Send /start message to your telegram bot\n----------------\n Have fun!\n -hosy')