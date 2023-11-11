import time
import datetime
import sqlite3

sleep_seconds=86400

while(True):
    conn = sqlite3.connect('D:/web/backend/db.sqlite3')
    cursor = conn.cursor()
    cursor.execute("UPDATE sducraft_notice SET valid = ? WHERE invalid_date < datetime('now', 'localtime', '+00:00')", (0,))
    conn.commit()
    conn.close()
    print(datetime.datetime.now())
    time.sleep(sleep_seconds)