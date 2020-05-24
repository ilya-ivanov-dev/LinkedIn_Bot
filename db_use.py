import sqlite3


def db_save(val):
    """ Creating a table (if it is not) and recording the received data """
    con = sqlite3.connect("db_LinkedIn.sqlite3")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Contacts (
      id INTEGER, 
      Date TEXT, 
      Time TEXT, 
      Name TEXT, 
      Job_position TEXT, 
      Geo TEXT, 
      href TEXT PRIMARY KEY NOT NULL,       
      Status TEXT
      )
    """)

    last_id = cur.execute('SELECT * FROM Contacts ORDER BY id DESC LIMIT 1').fetchone()
    if last_id == None:
        new_id = 1
    else:
        new_id = last_id[0] + 1

    cur.execute(f"""
      INSERT OR IGNORE INTO Contacts (id, Date, Time, Name, Job_position, Geo, href, Status)
      VALUES (
        '{new_id}',
        '{val.get('date')}',
        '{val.get('time')}', 
        '{val.get('name')}', 
        '{val.get('job')}', 
        '{val.get('geo')}', 
        '{val.get('href')}', 
        '{val.get('status')}'
        )
    """)

    con.commit()
    cur.close()
    con.close()
