import sqlite3
from datetime import datetime

DATABASE_NAME = 'project10a.db'

con = sqlite3.connect(f'{DATABASE_NAME}')
cur = con.cursor()

# insert dummy data
cur.execute(f"""
    INSERT INTO sensor_detection (timestamp)
    VALUES({datetime.utcnow().isoformat()}), ({datetime.utcnow().isoformat()});
    """)

cur.execute("""
    INSERT INTO photos (detection_id)
    VALUES (1), (2);
    """)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()
