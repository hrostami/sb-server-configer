import pickle
import os

os.system('systemctl stop cconfiger.service')
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

with open("/root/configer/user_data.pkl", "wb") as f:
    pickle.dump(user_data, f)
    print(f"-------user_data was created!-------\n{user_data}\n\n")
    os.system('systemctl restart configer.service')
