import requests
from datetime import datetime
import time
import subprocess
import os
import sqlite3
from PIL import Image

RESULT_PATH = "runs/detect/"
OUTPUT_IMAGE_PATH = "res/"

server_address = 'http://10.0.0.44/cam-hi.jpg'

con = sqlite3.connect('image.db')
cur = con.cursor()


def get_pic():
  try:
    response = requests.get(server_address, timeout=3)
  except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
    print("TIMEOUT at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
    return
  
  if response.status_code != 200:
    print("ERROR at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
    print("ERROR CODE: ", response.status_code)
    print(response.content())
    return
    
  image = response.content
  print("Received {} bytes".format(len(image)))

  filename = 'recv_img_{}.jpg'.format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))
  filename_raw = filename[:-4]

  with open('images/' + filename, 'wb') as f:
    f.write(image)
  
  print("Wrote image of size {} B".format(len(image)))

  # Run YoloV7 on the image here
  subprocess.run(["python3", "yolov7/detect.py", "--weights", "yolov7/yolov7-tiny.pt", "--conf", "0.25", "--source", 'images/' + filename, "--save-txt", "--name", filename_raw, "--no-trace"]) 
  subprocess.run(['rm', 'images/' + filename])

  # text file path
  # print(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt')
  # image path (after yolov7)
  # print(RESULT_PATH + filename)

  # Check result
  if os.path.exists(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt'):
    print("Opening txt at path={}".format(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt'))
    with open(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt', 'r') as file:
      personFound = False
      while True:
        line = file.readline()
        if not line:
          break
        values = line.split(' ')
        if values[0] == '0':
          personFound = True
          break
          
      if personFound:
        filename_new = filename[:-4] + '_person.jpg'
        print("Moving image with person to {}".format(OUTPUT_IMAGE_PATH + 'flagged/' + filename_new))
        subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'flagged/' + filename_new])
        cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'flagged/' + filename_new, datetime.now(), True))
      else:
        print("Moving image to {}".format(OUTPUT_IMAGE_PATH + 'unflagged/' + filename))
        subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
        cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'unflagged/' + filename, datetime.now(), False))
        print("Compressing image")
        subprocess.run(['jpegoptim', '--size=6k',  OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
  else:
    # No txt file found -> nothing was found in the picture
    print("Moving image to {}".format(OUTPUT_IMAGE_PATH + 'unflagged/' + filename))
    subprocess.run(['mv', RESULT_PATH + filename_raw + '/' + filename, OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
    cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'unflagged/' + filename, datetime.now(), False))
    print("Compressing image")
    subprocess.run(['jpegoptim', '--size=6k',  OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
  con.commit()

  # How do I delete it automatically in 30 days?
  #  Add a delete command in the main loop that does datetime.now() - 30 days, and checks filename at the current second and second-1
  #  If it finds a picture that is not marked, delete it
  # OR... add a crontab that runs every hour that runs a script that finds all files that are 
  #  images and older than a day and don't have a flag in their name and deletes them


while True:  
  get_pic()
  time.sleep(1)
