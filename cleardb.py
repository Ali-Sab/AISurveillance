import sqlite3

con = sqlite3.connect('image.db')
cur = con.cursor()

cur.execute('DELETE FROM image')
con.commit()

# note that the images are not deleted, only the db entries