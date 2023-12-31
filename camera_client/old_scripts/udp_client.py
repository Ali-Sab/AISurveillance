import socket
from datetime import datetime
import time
from json import load
import subprocess
import os
import sqlite3

RESULT_PATH = "runs/detect/"
OUTPUT_IMAGE_PATH = "res/"
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

con = sqlite3.connect('image.db')
cur = con.cursor()


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
  filename_raw = filename[:-4]

  with open('images/' + filename, 'wb') as f:
    f.write(image)
  
  print("Wrote image of size {} B".format(len(image)))
  if len(image) < 100:
    print(image)

  # Run YoloV7 on the image here
  subprocess.run(["python3", "yolov7/detect.py", "--weights", "yolov7/yolov7-tiny.pt", "--conf", "0.25", "--source", 'images/' + filename, "--save-txt", "--name", filename_raw]) 
  subprocess.run(['rm', 'images/' + filename])

  # text file path
  print(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt')
  # image path (after yolov7)
  print(RESULT_PATH + filename)
  # Check result
  if os.path.exists(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt'):

    file = open(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt', 'r')
    while True:
      line = file.readline()
      if not line:
        break
      values = line.split(' ')
      if values[0] == '0':
        filename_new = filename[:-4] + '_person.jpg'
        subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'flagged/' + filename_new])
        cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'flagged/' + filename_new, datetime.now(), True))
      else:
        subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
        cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'unflagged/' + filename, datetime.now(), False))
        subprocess.run(['jpegoptim', '--size=6k',  OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
      # if no human, run compress command on the output (which may have marked another animal) and write it out somewhere
      # in either case, delete the old copy
  else:
    # No txt file found -> nothing was found in the picture
    subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
    cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'unflagged/' + filename, datetime.now(), False))
    subprocess.run(['jpegoptim', '--size=6k',  OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
  con.commit()

  # How do I delete it automatically in 1 day?
  #  Add a delete command in the main loop that does datetime.now() - 1 day, and checks filename at the current second and second-1
  #  If it finds a picture that is not marked, delete it
  # OR... add a crontab that runs every hour that runs a script that finds all files that are 
  #  images and older than a day and don't have a flag in their name and deletes them


while True:
  try:
    get_pic()
  except socket.timeout:
    print("TIME OUT at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
  time.sleep(0.5)
   