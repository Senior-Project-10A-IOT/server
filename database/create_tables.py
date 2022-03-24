import sqlite3

DATABASE_NAME = 'project10a.db'

con = sqlite3.connect(f'{DATABASE_NAME}')
cur = con.cursor()

# Create table
cur.execute("""
    CREATE TABLE sensor_detection
    (id INTEGER PRIMARY KEY,
    timestamp datetime NOT NULL)
    """)

cur.execute("""
    CREATE TABLE photos
    (detection_id INTEGER NOT NULL,
    photo BLOB
    FOREIGN KEY(detection_id) REFERENCES sensor_detection(id))
    """)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
