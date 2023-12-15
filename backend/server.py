from flask import Flask, request, send_from_directory
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app)
server_path = 'http://localhost:5000/images/'

@app.route('/images/<path:path>')
def send_image(path):
    return send_from_directory('../camera_client/images', path)

@app.route("/live")
def live():
    entries = os.listdir('../camera_client/images/')
    entries = sorted(entries)

    datetime_format = "recv_img_%Y.%m.%d_%H.%M.%S.jpg"
    for i, entry in enumerate(entries):
        entries[i] = {'filepath':server_path + entry, 'datetime':datetime.strptime(entry, datetime_format).timestamp()}
    return entries

@app.route("/weekly-sightings")
def weekly_sightings():
    con = sqlite3.connect('../camera_client/image.db')
    cur = con.cursor()

    dates = []
    timenow = datetime.now()
    for i in range(5):
        dates.append(timenow - timedelta(weeks=i))

    sightings = []
    for i in range(4):
        cur.execute("SELECT COUNT(*) FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [dates[i+1], dates[i]])
        sightings.append({'sightings':cur.fetchall(), 'start_date':dates[i+1], 'end_date':dates[i]})
    
    return sightings

@app.route('/daily-sightings')
def daily_sightings():
    week = request.args.get('week', default=0, type=int)
    if isinstance(week, int) is False:
        return '<div>Param week should be a number.</div>'
    if week < 0:
        return '<div>Param week should be non-negative.</div>'
    
    con = sqlite3.connect('../camera_client/image.db')
    cur = con.cursor()

    dates = []
    timenow = datetime.now() - timedelta(weeks=week)
    sightings = []
    for i in range(8):
        dates.append(timenow - timedelta(days=i))

    for i in range(7):
        cur.execute("SELECT filename FROM image WHERE is_person=1 AND dt > ? AND dt < ?", [dates[i+1], dates[i]])
        results = cur.fetchall()
        image_path = '../camera_client/' + results[0][0] if len(results) > 0 else ""
        sightings.append({'sightings':len(results), 'start_date':dates[i+1], 'end_date':dates[i], 'image':image_path})

    return sightings

@app.route("/day-images")
def day_images():
    date = request.args.get('date', default=0, type=str)
    if isinstance(date, str) is False:
        return '<div>Param date should be a number.</div>'
    if date < 0:
        return '<div>Param date should be non-negative.</div>'
    sightings = []

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
