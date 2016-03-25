from views import db
from _config import DATABASE_PATH

import sqlite3
from datetime import datetime

with sqlite3.connect(DATABASE_PATH) as connection:
    c = connection.cursor()
    c.execute("""ALTER TABLE tasks RENAME TO old_tasks""")
    db.create_all()
    c.execute("""Select name, due_date, priority, status
        from old_tasks order by task_id asc""")
    data = [(row[0], row[1], row[2], row[3], datetime.now(), 1) for row in c.fetchall()]
    c.executemany("""Insert into tasks (name, due_date, priority, status, 
        posted_date, user_id) values (?, ?, ?, ?, ?, ?)""", data)
    c.execute("""DROP TABLE old_tasks""")

