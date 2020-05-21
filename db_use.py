import sqlite3


# Запись данных в таблицу
def db_save(contacts):
    con = sqlite3.connect("db_LinkedIn.sqlite3")
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Contacts (   Date TEXT, '
                                                        'Time TEXT, '
                                                        'Name TEXT, '
                                                        'Job_position TEXT, '
                                                        'href TEXT, '
                                                        'Geo TEXT, '
                                                        'Status TEXT)')

    cur.executemany('INSERT INTO Contacts VALUES (?,?,?,?,?,?,?)', contacts)
    con.commit()
    cur.close()
    con.close()
