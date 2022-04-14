import sqlite3
from datetime import datetime

conn = sqlite3.connect('project10a.db')
cursor = conn.cursor()

with open("motion.jpg", "rb") as input_file:
    ablob = input_file.read()
    cursor.execute("INSERT INTO past_events (timestamp, photo) VALUES(?, ?)", [(f'{datetime.utcnow().isoformat()}', sqlite3.Binary(ablob),)])
    conn.commit()

# with open("Output.bin", "wb") as output_file:
#     cursor.execute("SELECT file FROM past_events WHERE id = 0")
#     ablob = cursor.fetchone()
#     output_file.write(ablob[0])

cursor.close()
conn.close()
