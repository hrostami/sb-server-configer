import json
import subprocess
import os
import pickle
import datetime
import base64
import requests
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


# Loading User Data from file
def open_user_data():
    if os.path.exists("/root/user_data.pkl"):
        with open("/root/user_data.pkl", "rb") as file:
            user_data = pickle.load(file)
    else:
        user_data = {'chat_id':'', 'user_id':'', 'channel_id':'', 'server_IP':'',
                    'bot_token':'', 'listen_port':443, "renewal_interval":3600, "domain_name":'domain.com'}
    return user_data
user_data = open_user_data()

# Define the server IP and Telegram bot token as a global variable
SERVER_IP = user_data['server_IP']
BOT_TOKEN = user_data['bot_token']

# Define a function to get the location of the server
def iploc():
    url = 'http://ip-api.com/json/'
    r = requests.get(url)
    iploc = r.json()['country']
    return iploc

# Define a function to save the modified json data to a file
def save_to_file(data, mode='json', path=''):
    if mode == 'json':
        with open('/usr/local/etc/sing-box/config.json', 'w') as file:
            json.dump(data, file)
    elif mode == 'pkl':
        with open(path, 'wb') as f:
            pickle.dump(data, f)

# Define  a function to renew uuid, private_key and short_id automatically everyday and send the new config
def renew_data():
    # Run shell commands to generate UUID, reality keypair, and short ID
    uuid = subprocess.run(["/usr/local/bin/sing-box", "generate", "uuid"], capture_output=True, text=True).stdout.strip()
    reality_keypair = subprocess.run(["/usr/local/bin/sing-box", "generate", "reality-keypair"], capture_output=True, text=True).stdout.strip().splitlines()
    private_key = reality_keypair[0].split(": ")[1]
    public_key = reality_keypair[1].split(": ")[1]
    short_id = subprocess.run(["/usr/local/bin/sing-box", "generate", "rand", "--hex", "8"], capture_output=True, text=True).stdout.strip()

    with open("/root/sb-data.json", "w") as f:
        dic = {"uuid":uuid, "public_key":public_key, "private_key":private_key, "short_id":short_id}
        json.dump(dic,f)

    # Save public key to a pickle file
    with open("/root/public_key.pkl", "wb") as f:
        pickle.dump(public_key, f)

    # Stopping sing-box before editing config, not doing it for first config setup though!
    try:
        subprocess.run(["systemctl", "stop", "sing-box"])
    except Exception as e:
        print(f'Error happened stopping sing-box:\n{e}')
    
    # Load the JSON data
    json_data = open_config_json()

    # Modify the values in the JSON data
    json_data["inbounds"][0]["users"][0]["uuid"] = uuid
    json_data["inbounds"][0]["tls"]["reality"]["private_key"] = private_key
    json_data["inbounds"][0]["tls"]["reality"]["short_id"] = [short_id]
    
    # Save the modified JSON data to config
    save_to_file(json_data)

    # Restarting sing-box
    try:
        subprocess.run(["systemctl", "restart", "sing-box"])
    except Exception as e:
        print(f'Error happened restarting sing-box:\n{e}')
    
    return json_data

# Define the json data to be modified
def open_config_json():
    if os.path.exists("/usr/local/etc/sing-box/config.json"):
        with open("/usr/local/etc/sing-box/config.json", "r") as file:
            json_data = json.load(file)
    else:
        json_data = {
                        "log": {
                            "level": "info",
                            "timestamp": True
                        },
                        "inbounds": [
                            {
                                "type": "vless",
                                "tag": "vless-in",
                                "listen": "::",
                                "listen_port": user_data['listen_port'],
                                "sniff": True,
                                "sniff_override_destination": True,
                                "domain_strategy": "ipv4_only",
                                "users": [
                                    {
                                        "uuid": "E66E8785-9284-493D-BF48-8232AA3686EA", 
                                        "flow": "xtls-rprx-vision"
                                    }
                                ],
                                "tls": {
                                    "enabled": True,
                                    "server_name": "www.datadoghq.com",
                                    "reality": {
                                        "enabled": True,
                                        "handshake": {
                                            "server": "www.datadoghq.com",
                                            "server_port": 443
                                        },
                                        "private_key": "qAdSu-xtsEOlP-xfysiAdiU-NxUBWmxZ63OOnTEMFFk",
                                        "short_id": [ 
                                            "6ba85179e30d4fc2"
                                        ]
                                    }
                                }
                            }
                        ],
                        "outbounds": [
                            {
                                "type": "direct",
                                "tag": "direct"
                            },
                            {
                                "type": "block",
                                "tag": "block"
                            }
                        ]
                    }
        save_to_file(json_data)
        json_data = renew_data()
        os.system('systemctl enable --now sing-box')
    return json_data
json_data = open_config_json()

# Define a function to replace the data
def replace_data(server, server_name):
    json_data = open_config_json()
    json_data['inbounds'][0]['tls']['server_name'] = server_name
    json_data['inbounds'][0]['tls']['reality']['handshake']['server'] = server
    return json_data

# Define function for scheduled renewal
def renew_config(context: CallbackContext):
    # Define chat_id
    user_data = open_user_data()
    chat_id = user_data['user_id']
    if user_data['chat_id'] == 'ch':
        channel_id = user_data['channel_id']
    else:
        channel_id = user_data['user_id']

    # Do the renewing process
    renew_data()

    # Send new config to user
    message, encoded64 = generate_vless_config_string()
    context.bot.send_message(chat_id=chat_id, text=message)
    context.bot.send_message(chat_id=channel_id, text=encoded64)

def generate_vless_config_string():
    # check to see if public_key exists
    if not os.path.exists("/root/public_key.pkl"):
        renew_data()
    # Load the modified JSON data from the file
    json_data = open_config_json()

    # Extract the necessary data from the JSON data
    uuid = json_data["inbounds"][0]["users"][0]["uuid"]
    listen_port = json_data["inbounds"][0]["listen_port"]
    server_name = json_data["inbounds"][0]["tls"]["server_name"]
    short_id = json_data["inbounds"][0]["tls"]["reality"]["short_id"][0]
    with open("/root/public_key.pkl", "rb") as file:
        public_key = pickle.load(file)
    # Generate the VLESS proxy configuration string
    loc= iploc()
    config_string =( f"vless://{uuid}@{SERVER_IP}:{listen_port}?security=reality&"
                    f"sni={server_name}&fp=chrome&pbk={public_key}&sid={short_id}&"
                    f"type=tcp&flow=xtls-rprx-vision#sb-{loc}")
    # CREATE BASE64
    encodedBytes = base64.b64encode(config_string.encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")

    # Change web-page if exists
    domain = user_data['domain_name']
    if os.path.exists(f"/var/www/{domain}/html/index.html"):
        with open(f"/var/www/{domain}/html/index.html", "w") as file:
            file.write(encodedStr)

    return config_string, encodedStr

# Define a function to handle the /replace command
def replace_handler(update, context):
    user_data = open_user_data()
    chat_id = update.message.chat_id
    if user_data['chat_id'] == 'ch':
        channel_id = user_data['channel_id']
    else:
        channel_id = chat_id
    text = update.message.text.split()
    if chat_id == user_data['user_id']:
        if len(text) == 2:
            server = text[1]
            server_name = text[1]
            modified_data = replace_data(server, server_name)
            subprocess.run(["systemctl", "stop", "sing-box"])
            save_to_file(modified_data)
            subprocess.run(["systemctl", "restart", "sing-box"])
            context.bot.send_message(chat_id=chat_id, text="Data replaced successfully!")
            message, encoded64 = generate_vless_config_string()
            context.bot.send_message(chat_id=channel_id, text=encoded64)
            context.bot.send_message(chat_id=chat_id, text=message)
        else:
            context.bot.send_message(chat_id=chat_id, text="Invalid command format. Usage: /replace domain-name.com")
    else:
        context.bot.send_message(chat_id=chat_id, text="You're not allowed to send SNI to this bot, piss off!")

# Define status handler
def status_handler(update, context):
    user_data = open_user_data()
    chat_id = update.message.chat_id
    process = update.message.text.split()[1]
    if chat_id == user_data['user_id']:
        status = subprocess.run(["systemctl", "status", process], capture_output=True, text=True).stdout.strip()
        context.bot.send_message(chat_id=chat_id, text=status)

# Define command handler
def command_handler(update, context):
    user_data = open_user_data()
    chat_id = update.message.chat_id
    command = update.message.text.split()[1:]
    if chat_id == user_data['user_id']:
        output = subprocess.run(command, capture_output=True, text=True).stdout.strip()
        with open(f"/root/output.txt", "w") as file:
            file.write(output)
        update.message.reply_document(
        document=open("/root/output.txt", "r"),
        filename="output.txt",
        caption="Here's the output of the command you asked! "
                            )

# Define start handler to send the config 
def start_handler(update, context):
    user_data = open_user_data()
    chat_id = update.message.chat_id
    if user_data['chat_id'] == 'ch':
        channel_id = user_data['channel_id']
    else:
        channel_id = chat_id
    if len(str(user_data['user_id'])) == 0 :
        user_data['user_id'] = chat_id
        with open(f"/root/user_data.pkl", "wb") as file:
            pickle.dump(user_data, file)
        context.bot.send_message(chat_id=chat_id, text='Your Id is saved.\nPlease send /set command to set parameters.')
    elif chat_id == user_data['user_id']:
        renew_data()
        message, encoded64 = generate_vless_config_string()
        context.bot.send_message(chat_id=channel_id, text=encoded64)
        context.bot.send_message(chat_id=chat_id, text=message)
    else:
        message ='You are not allowed to send messages to this bot'
        context.bot.send_message(chat_id=chat_id, text=message)
 
# Define status handler
def user_data_handler(update, context):
    chat_id = update.message.chat_id
    input = update.message.text.split()
    user_data = open_user_data()
    if chat_id == user_data['user_id']:
        if len(input) == 3:
            param = input[1]
            if param in ('channel_id', 'renewal_interval','listen_port'):
                value = int(input[2])
            else:
                value = input[2]
            user_data[param] = value
            save_to_file(user_data, 'pkl', '/root/user_data.pkl')
            context.bot.send_message(chat_id=chat_id, text=f'{param} set to {value}')
        else:
            context.bot.send_message(chat_id=chat_id, text="لطفا به شکل زیر پیام بفرستید، اول پارامتر مد نظر بعد فاصله و بعد مقدار. هر پارامتر رو جدا بفرستید")
            message = ("/set chat_id me یا ch\n"
                        "/set channel_id گرفتید myidbot آیدی کانال که از بات\n" 
                        "/set server_IP آی پی سرور تون\n" 
                        "/set listen_port پورت سینگ باکس مثلا 443\n" 
                        "/set bot_token توکن بات تلگرام\n"
                        "/set renewal_interval زمان تجدید کانفیگ به ساعت\n"
                        "/set domain_name دامنه در صورت وجود" )
            context.bot.send_message(chat_id=chat_id, text=message)
   


# Function to handle errors
def error(bot, context):
    print(f"bot {bot} caused error {context.error}")

# Define the main function
def main():
    # Create a telegram bot and add a command handler for /replace command
    updater = Updater(BOT_TOKEN)
    j = updater.job_queue
    print('Bot started')
    try:
        j.run_repeating(renew_config, user_data['renewal_interval']*3600)
    except Exception as e:
        print(f'Error happened during renew:\n{e}')
    updater.dispatcher.add_handler(CommandHandler('replace', replace_handler))
    updater.dispatcher.add_handler(CommandHandler('status', status_handler))
    updater.dispatcher.add_handler(CommandHandler('run', command_handler))
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('set', user_data_handler))
    updater.dispatcher.add_error_handler(MessageHandler(Filters.all, error))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
