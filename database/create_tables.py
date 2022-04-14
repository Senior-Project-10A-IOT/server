import sqlite3

DATABASE_NAME = 'project10a.db'

con = sqlite3.connect(f'{DATABASE_NAME}')
cur = con.cursor()

cur.execute("""
    CREATE TABLE past_events
    (id INTEGER PRIMARY KEY,
    timestamp datetime NOT NULL,
    photo BLOB)
    """)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
