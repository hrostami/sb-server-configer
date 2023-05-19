import os


print('--------> Downloading configer.py\n\n')
os.system('curl -Lo /root/configer/configer.py https://raw.githubusercontent.com/hrostami/sb-server-configer/master/configer.py')
os.system('systemctl restart configer.service')
print('Done, enjoy!')
