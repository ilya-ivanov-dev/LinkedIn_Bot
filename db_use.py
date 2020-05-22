import sqlite3


def db_save(val):
    """ Creating a table (if it is not) and recording the received data """
    con = sqlite3.connect("db_LinkedIn.sqlite3")
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS Contacts (
      Id INTEGER PRIMARY KEY AUTOINCREMENT, 
      Date TEXT, 
      Time TEXT, 
      Name TEXT, 
      Job_position TEXT, 
      href TEXT, 
      Geo TEXT, 
      Status TEXT
      )
    """)

    cur.execute(f"""
      INSERT INTO Contacts (Date, Time, Name, Job_position, href, Geo, Status)
      VALUES (
        '{val.get('date')}', 
        '{val.get('time')}', 
        '{val.get('name')}', 
        '{val.get('job')}', 
        '{val.get('href')}', 
        '{val.get('geo')}', 
        '{val.get('status')}'
        )
    """)

    con.commit()
    cur.close()
    con.close()
