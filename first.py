import pickle
import os
import subprocess
from subprocess import Popen, PIPE
import time

# Get sing-box v1.3 beta11 and place it in root
print('--------> Downloading sing-box:\n\n\n\n')
subprocess.run(["bash", "-c", "curl -Ls https://raw.githubusercontent.com/FranzKafkaYu/sing-box-yes/master/install.sh | bash -s install 1.3-beta11"], check=True)
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
    "renewal_interval":3600,
    "domain_name":'domain.com'

}
user_data["chat_id"] = input("\nYou want the bot to send messages to channel or you?\n----> Type  me or ch: ")
while not user_data["chat_id"] in ('me', 'ch'):
    user_data["chat_id"] = input("\n----> Please type  me or ch: ")
user_data["server_IP"] = input("Enter server IP: ")
user_data["listen_port"] = int(input("Enter port number: "))
user_data["channel_id"] = input("Enter channel ID you got from @myidbot: ")
user_data["bot_token"] = input("Enter bot token: ")
user_data["renewal_interval"] = int(input("Enter renewal interval in HOURS: "))
user_data["domain_name"] = input("Enter domain name if you have one, if not just press Enter: ")

with open("/root/user_data.pkl", "wb") as f:
    pickle.dump(user_data, f)
    print(f"-------user_data was created!-------\n{user_data}\n\n")

print('--------> Downloading configer.py\n\n')
os.system('curl -Lo /root/configer.py https://raw.githubusercontent.com/hrostami/sb-server-configer/master/configer.py')
os.system('curl -Lo /root/user_data_editor.py https://raw.githubusercontent.com/hrostami/sb-server-configer/master/user_data_editor.py')
os.system('systemctl daemon-reload')
os.system('apt-get install pip')
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
default_config_path = '/usr/local/etc/sing-box/config.json'
if os.path.exists(default_config_path):
    os.system(f'rm {default_config_path}')
print('--------Setting up Services finished --------\n\n')

s = '''
  _____        _               _____                ___       _                       _                       
 | ____|_ __  (_) ___  _   _  |  ___| __ ___  ___  |_ _|_ __ | |_ ___ _ __ _ __   ___| |_                     
 |  _| | '_ \ | |/ _ \| | | | | |_ | '__/ _ \/ _ \  | || '_ \| __/ _ \ '__| '_ \ / _ \ __|                    
 | |___| | | || | (_) | |_| | |  _|| | |  __/  __/  | || | | | ||  __/ |  | | | |  __/ |_ _                   
 |_____|_| |_|/ |\___/ \__, | |_|  |_|  \___|\___| |___|_| |_|\__\___|_|  |_| |_|\___|\__( )                  
            |__/       |___/                                                             |/                   
                                _   _                                                                         
                               | | | | ___  ___ _   _                                                         
                               | |_| |/ _ \/ __| | | |                                                        
                               |  _  | (_) \__ \ |_| |                                                        
                               |_| |_|\___/|___/\__, |                                                        
                                                |___/                                                         
'''

print(s)
print('\n\n-------->  Send /start message to your telegram bot')
