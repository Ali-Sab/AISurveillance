import subprocess
import os

RESULT_PATH = "runs/detect/"

filename = 'recv_img_2023.11.08_18.35.18.jpg'
filename_raw = filename[:-4]

# Run YoloV7 on the image here
subprocess.run(["python3", "yolov7/detect.py", "--weights", "yolov7/yolov7-tiny.pt", "--conf", "0.25", "--source", filename, "--save-txt", "--name", filename_raw]) 

print(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt')
# Check result
if os.path.exists(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt'):

  file = open(RESULT_PATH + filename_raw + '/labels/' + filename_raw + '.txt', 'r')
  while True:
    line = file.readline()
    if not line:
      break
    values = line.split(' ')
    if values[0] == '0':
      print("FLAGGING")
else:
  print("no file")