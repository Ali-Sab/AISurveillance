import socket
from datetime import datetime
import time

passcode = 'OdiJ4Hpa5c'

bytes_to_send = str.encode(passcode)
server_address_port = ("10.0.0.44", 5030)
buffer_size = 1436
fd = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def get_pic():
  fd.sendto(bytes_to_send, server_address_port)

  msg = fd.recvfrom(buffer_size)
  if msg[0] == "ERROR":
     return
  
  msg_length = len(msg[0])
  image = msg[0]
  print("Received {} bytes".format(msg_length))

  while msg_length == buffer_size:
    msg = fd.recvfrom(buffer_size)
    msg_length = len(msg[0])
    image += msg[0]
    print("Received {} bytes".format(msg_length))

  img_data = image
  filename = 'recv_img_{}.jpg'.format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))

  with open(filename, 'wb') as f:
      f.write(img_data)

get_pic()

while True:
  get_pic()
  time.sleep(2)
   