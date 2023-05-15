import os 

# Remove files
files = ["/root/configer/user_data.pkl",
          "/root/configer/sb-data.json",
          "/root/configer/public_key.pkl",
          "/usr/local/etc/sing-box/config.json",
          "/root/configer/configer.py",
          "/root/configer/first.py",

          ]
for path in files:
    if os.path.exists(path):
            os.system(f'rm {path}')
            print(f'Delted {path}\n')

# Stop Services
try:
    os.system('systemctl stop configer')
    os.system('systemctl stop sing-box')
except Exception as e:
      print(e)