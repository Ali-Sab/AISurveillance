from flask import Flask
import sqlite3
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route("/weekly-sightings")
def weekly_sightings():
    con = sqlite3.connect('../camera_client/image.db')
    cur = con.cursor()

    timenow = datetime.now()
    thisweek = timenow - timedelta(days=7)
    lastweek = timenow - timedelta(days=14)
    lastweek2 = timenow - timedelta(days=21)
    lastweek3 = timenow - timedelta(days=28)
    sightings = []
    cur.execute("SELECT COUNT(*) FROM image WHERE is_person=1 AND dt > ?", [thisweek])
    sightings.append({'sightings':cur.fetchall(), 'start_date':thisweek, 'end_date':timenow})

    cur.execute("SELECT COUNT(*) FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [lastweek, thisweek])
    sightings.append({'sightings':cur.fetchall(), 'start_date':lastweek, 'end_date':thisweek})

    cur.execute("SELECT COUNT(*) FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [lastweek2, lastweek])
    sightings.append({'sightings':cur.fetchall(), 'start_date':lastweek2, 'end_date':lastweek})

    cur.execute("SELECT COUNT(*) FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [lastweek3, lastweek2])
    sightings.append({'sightings':cur.fetchall(), 'start_date':lastweek3, 'end_date':lastweek2})
    
    return sightings

@app.route('/daily-sightings')
def daily_sightings():
    con = sqlite3.connect('../camera_client/image.db')
    cur = con.cursor()

    dates = []
    timenow = datetime.now()
    sightings = []
    for i in range(8):
        dates.append(timenow - timedelta(days=i))

    for i in range(7):
        cur.execute("SELECT filename FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [dates[i+1], dates[i]])
        results = cur.fetchall()
        image_path = '../camera_client/' + results[0][0] if len(results) > 0 else ""
        sightings.append({'sightings':len(results), 'start_date':dates[i+1], 'end_date':dates[i], 'image':image_path})

    return sightings


# for i, result in enumerate(results):
#         results[i] = list(results[i])
#         results[i][0] = '../camera_client/' + result[0]
# /live
# frontend pings backend, backend creates tcp socket with frontend using socketio "Flask-SocketIO" may work
# whenever backend sends a new path, frontend sees it and updates the path on their end
# frontend finds the new image and displays it


# /recordings
# purpose: retain all data from now to last 28 days and send to frontend




# /archive
# purpose: keep images for sightings older than 30 days
# frontend tells users how many sightings per month, then shows sightings per day in a slider mode
