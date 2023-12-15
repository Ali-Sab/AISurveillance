import sqlite3
from datetime import datetime
from datetime import timedelta
import logging
import os

daysToKeep = 28 # how many days are considered "recent"

formattedTime = datetime.now().strftime('%Y.%m.%d')
logging.basicConfig(filename="logs/http_client_" + formattedTime + ".log", filemode='a', encoding='utf-8', level=logging.DEBUG)

con = sqlite3.connect('image.db')
cur = con.cursor()

# We wish to remove images that are 28 days old if no person is in the image
logging.debug("DELETION EVENT: Time is now {}".format(datetime.now()))
dt = datetime.now() - timedelta(days=daysToKeep)
logging.debug("Deleting all images before time = {}".format(dt))

cur.execute("SELECT filename FROM image WHERE is_person=0 AND dt < ?", [dt])
results = cur.fetchall()
cur.execute("DELETE FROM image WHERE is_person=0 AND dt < ?", [dt])
con.commit()

for result in results:
	filename = result[0]
	logging.debug("Deleting image: {}".format(filename))
	try:
		os.remove(filename)
	except FileNotFoundError as e:
		logging.warning(e)
		continue

