import sqlite3

login_value = input()
connection = sqlite3.connect('Login_data.db')
cursor = connection.cursor()
login_list = []
cursor.execute('SELECT Login FROM Login_data')
for i in cursor:
    login_list.append(i[0])
if login_value not in login_list:
    query = f"INSERT INTO Login_data (Login, Password) VALUES ('{login_value}', '{password_value}');"
    cursor.execute(query)
    connection.commit()

cursor.close()
connection.close()