import socket
from datetime import datetime
import time
from json import load

# load passcode from config json in the same directory
passcode = '*********'
with open('config.json') as f:
    data = load(f)
    passcode = str(data['PASSCODE'])

bytes_to_send = str.encode(passcode)
server_address_port = ("10.0.0.44", 5030)
# 1436 is a number acquired from experimenting with the packet size sent by the esp32-cam module that is sending the images
buffer_size = 1436
fd = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
fd.settimeout(2)


def get_pic():
  fd.sendto(bytes_to_send, server_address_port)

  msg = fd.recvfrom(buffer_size)
  if len(msg[0]) == 5 and msg[0].decode('ASCII') == "ERROR":
    print("ERROR at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
    return
  
  msg_length = len(msg[0])
  image = msg[0]
  print("Received {} bytes".format(msg_length))

  while msg_length == buffer_size:
    msg = fd.recvfrom(buffer_size)
    msg_length = len(msg[0])
    image += msg[0]
    print("Received {} bytes".format(msg_length))

  filename = 'recv_img_{}.jpg'.format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))

  with open(filename, 'wb') as f:
    f.write(image)
  
  print("Wrote image of size {} B".format(len(image)))
  if len(image) < 100:
    print(image)


while True:
  try:
    get_pic()
  except socket.timeout:
    print("TIME OUT at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
  time.sleep(2)
   