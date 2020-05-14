import sqlite3


conn = sqlite3.connect("db_LinkedIn.sqlite3")
cursor = conn.cursor()

# Создание таблицы БД: | № | Дата | Имя | Должность | Ссылка | Гео |
# cursor.execute("""CREATE TABLE Contacts
#                   (Number integer, Date text, Name text,
#                   Job_position text, href text, Geo text)""")

# Вставляем данные в таблицу
cursor.execute("""INSERT INTO Contacts
                  VALUES ()""")




conn.close()
