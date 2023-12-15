import subprocess
from datetime import datetime
import os
from os import listdir
from os.path import isfile, join
import sqlite3
import logging

con = sqlite3.connect('image.db')
cur = con.cursor()

RESULT_PATH = "runs/detect/"
OUTPUT_IMAGE_PATH = "res/"
INPUT_IMAGE_PATH = "images/"
formattedTime = datetime.now().strftime('%Y.%m.%d')

logging.basicConfig(filename="logs/run_yolov7_" + formattedTime + ".log", filemode='a', encoding='utf-8', level=logging.DEBUG)

formattedTime = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')

onlyfiles = [f for f in listdir(INPUT_IMAGE_PATH) if isfile(join(INPUT_IMAGE_PATH, f))]
logging.debug("Found the following images: {}".format(onlyfiles))

imgPath = 'image_set_' + formattedTime
subprocess.run(['mkdir', imgPath])
for filename in onlyfiles:
	subprocess.run(['mv', 'images/' + filename, imgPath])

expName = "exp_" + formattedTime
expPath = RESULT_PATH + expName


subprocess.run(["python3", "yolov7/detect.py", "--weights", "yolov7/yolov7-tiny.pt", "--conf", "0.25", "--source", imgPath, "--save-txt", "--name", expName, "--no-trace"])
subprocess.run(['rm', '-rf', imgPath])

onlyfiles = [f for f in listdir(expPath) if isfile(join(expPath, f))]
logging.debug("Processed these images: {}".format(onlyfiles))

for filename in onlyfiles:
	logging.debug("Checking file: {}".format(filename))
	dt = datetime.strptime(filename, 'recv_img_%Y.%m.%d_%H.%M.%S.jpg')
	filename_raw = filename[:-4]

	# Check result
	personFound = False
	if os.path.exists(expPath + '/labels/' + filename_raw + '.txt'):
		logging.debug("Opening txt at path: {}".format(expPath + '/labels/' + filename_raw + '.txt'))
		with open(expPath + '/labels/' + filename_raw + '.txt', 'r') as file:
			personFound = False
			while True:
				line = file.readline()
				if not line:
					break
				values = line.split(' ')
				if values[0] == '0':
					personFound = True
					break
            
	# If no txt file found, then no person in image
	if personFound:
			filename_new = filename_raw + '_person.jpg'
			logging.debug("Moving image with person to {}".format(OUTPUT_IMAGE_PATH + 'flagged/' + filename_new))
			subprocess.run(['mv', expPath + "/" + filename, OUTPUT_IMAGE_PATH + 'flagged/' + filename_new])
			cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'flagged/' + filename_new, dt, True))
	else:
			logging.debug("Moving image to {}".format(OUTPUT_IMAGE_PATH + 'unflagged/' + filename))
			subprocess.run(['mv', expPath + "/" + filename, OUTPUT_IMAGE_PATH + 'unflagged/' + filename])
			cur.execute("INSERT INTO image VALUES(?, ?, ?)", (OUTPUT_IMAGE_PATH + 'unflagged/' + filename, dt, False))
			logging.debug("Compressing image")
			subprocess.run(['jpegoptim', '--size=6k',  OUTPUT_IMAGE_PATH + 'unflagged/' + filename])

	con.commit()