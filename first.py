import pickle
import os
import subprocess
import time

# Get sing-box v1.3 beta11 and place it in root
print('--------> Downloading sing-box:\n\n!!!! Enter 1 when it asks for input !!!!\n\n')
time.sleep(5)
# subprocess.run(['bash', '-c', 'curl -Ls https://raw.githubusercontent.com/FranzKafkaYu/sing-box-yes/master/install.sh | bash'], check=True, text=True, input='1\n')
cmd = "bash <(curl -Ls https://raw.githubusercontent.com/FranzKafkaYu/sing-box-yes/master/install.sh)"
p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate(input=b"1\n")
print(out.decode())
print(err.decode())
print('--------Installing sing-box finished--------\n\n')



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

os.system('curl -Lo /root/configer.py https://raw.githubusercontent.com/hrostami/sb-server-configer/remote/configer.py')
os.system('pip install python-telegram-bot==13.5')
os.system('pip install requests')
time.sleep(1)
print('--------> Setting up Services \n\n')
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
os.system('systemctl stop sing-box')
os.system('rm /usr/local/etc/sing-box/config.json')
print('--------Setting up Services finished --------\n\n')
print('-------->  Send /start message to your telegram bot\n----------------\n Have fun!\n -hosy')