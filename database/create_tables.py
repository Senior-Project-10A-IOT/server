import sqlite3

DATABASE_NAME = 'project10a.db'

con = sqlite3.connect(f'{DATABASE_NAME}')
cur = con.cursor()

# Create table
cur.execute(f"""
    CREATE TABLE sensor_detection
    (id INTEGER PRIMARY KEY,
    timestamp datetime NOT NULL)
    """)

cur.execute(f"""
    CREATE TABLE photos
    (motion_id INTEGER NOT NULL,
    photo BLOB NOT NULL)
    """)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
