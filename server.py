from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sqlite3


def authorize(client, client_address):
    result = False
    while not result:
        login_value = client.recv(BUFSIZ).decode("utf8")
        password_value = client.recv(BUFSIZ).decode("utf8")
        # print(login_value)
        # print(password_value)
        login_list = []
        password_list = []
        connection = sqlite3.connect('Login_data.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Login FROM Login_data')
        for i in cursor:
            login_list.append(i[0])
        cursor.execute('SELECT Password FROM Login_data')
        #print(login_list)
        #print(password_list)
        for i in cursor:
            password_list.append(i[0])
        for i in range(len(login_list)):
            if login_value == login_list[i]:
                # print(password_list)
                # print(password_value in password_list)
                if password_value == password_list[i]:
                    result = True
    client.send(bytes('go_open_chat_page', "utf8"))
    Thread(target=handle_client, args=(client, client_address, result,)).start()


def sending(client, client_address):
    result = False
    login_value = client.recv(BUFSIZ).decode("utf8")
    password_value = client.recv(BUFSIZ).decode("utf8")
    # print(login_value)
    # print(password_value)
    if login_value != '' and password_value != '':
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
        result = True
        if login_value not in login_list:
            client.send(bytes('go_open_start_page', "utf8"))
            Thread(target=choose, args=(client, client_address,)).start()


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print(f"{client_address} соединено")
        client.send(bytes("Добро пожаловать , введите своё имя и нажмите Enter", "utf8"))
        addresses[client] = client_address
        # client_socket.send(bytes(self.login_value, "utf8"))
        Thread(target=choose, args=(client, client_address,)).start()

def choose(client, client_address):
    name = client.recv(BUFSIZ).decode("utf8")
    #print(name)
    if name == "open_auth_page":
        Thread(target=authorize, args=(client, client_address,)).start()
    elif name == "open_reg_page":
        Thread(target=sending, args=(client, client_address,)).start()


def handle_client(client, client_address, result, ):
    # print(result)
    if result:
        name = "q"
        #name = client.recv(BUFSIZ).decode("utf8")
        msg = "%s вступил в переписку" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name

        while True:
            msg = client.recv(BUFSIZ).decode("utf8")
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name + ": ")
            else:
                print(f"{client_address} отключено")
                client.close()
                del clients[client]
                broadcast(bytes("%s покинул переписку" % name, "utf8"))
                break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + bytes(msg, "utf8"))


clients = {}
addresses = {}

HOST = '176.59.151.3'
PORT = 80
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("ожидание соединения")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
