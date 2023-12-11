import os
path = "images"
# Check whether the specified path exists or not
isExist = os.path.exists(path)
if not isExist:

   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")


import sqlite3

con = sqlite3.connect('image.db')
cur = con.cursor()

cur.execute("CREATE TABLE image(filename TEXT, dt datetime, is_person boolean)")
con.commit()

cur.execute("PRAGMA table_info('image')")
cur.fetchall()

print("Done")
