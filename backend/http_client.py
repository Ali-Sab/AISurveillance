import requests
from datetime import datetime
import time
import subprocess
import logging 

server_address = 'http://10.0.0.44/cam-hi.jpg'

OUTPUT_IMAGE_PATH = "images/"
formattedTime = datetime.now().strftime('%Y.%m.%d')
logging.basicConfig(filename="logs/http_client_" + formattedTime + ".log", filemode='a', encoding='utf-8', level=logging.DEBUG)

count = 0
def get_pic():
  try:
    response = requests.get(server_address, timeout=3)
  except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
    logging.error("TIMEOUT at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
    logging.error(e)
    return
  
  if response.status_code != 200:
    logging.error("ERROR at {}".format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S')))
    logging.error("ERROR CODE: ", response.status_code)
    logging.error(response.content())
    return
    
  image = response.content
  logging.debug("Received {} bytes".format(len(image)))

  filename = 'recv_img_{}.jpg'.format(datetime.now().strftime('%Y.%m.%d_%H.%M.%S'))

  with open(OUTPUT_IMAGE_PATH + filename, 'wb') as f:
    f.write(image)
  
  logging.debug("Wrote image of size {} B".format(len(image)))
  
  global count
  count += 1

  # How do I delete it automatically in 30 days?
  #  Add a delete command in the main loop that does datetime.now() - 30 days, and checks filename at the current second and second-1
  #  If it finds a picture that is not marked, delete it
  # OR... add a crontab that runs every hour that runs a script that finds all files that are 
  #  images and older than a day and don't have a flag in their name and deletes them


while True:  
  get_pic()
  time.sleep(3)
  if count >= 20:
    subprocess.Popen(['python3', 'run_yolov7.py'])
    subprocess.Popen(['python3', 'deleteOldImages.py'])
    count = 0
