import os 

# Remove files
files = ["/root/user_data.pkl",
          "/root/sb-data.json",
          "/root/public_key.pkl",
          "/root/sing-box_config.json",
          "/root/configer.py",
          "/root/first.py",

          ]
for path in files:
    if os.path.exists(path):
            os.system(f'rm {path}')
            print(f'Delted {path}\n')

# Stop Services
try:
    os.system('systemctl stop configer.services')
    os.system('systemctl stop sing-box')
except Exception as e:
      print(e)

# Remove sing-box
if os.path.exists('/root/sing-box'):
      os.system('rm -r /root/sing-box')
      os.system('systemctl disable sing-box')