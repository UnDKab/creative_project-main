import Start_page, Registration_page, Enter_page, New_chat_3
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3, sys
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


class StartWindow(QtWidgets.QMainWindow, Start_page.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.open_enter_page)
        self.pushButton_2.clicked.connect(self.open_reg_page)

    def open_enter_page(self):
        client_socket.send(bytes("open_auth_page", "utf8"))
        w1.show()
        w.hide()

    def open_reg_page(self):
        client_socket.send(bytes("open_reg_page", "utf8"))
        w2.show()
        w.hide()


class EnterWindow(QtWidgets.QMainWindow, Enter_page.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.check_enter)
        # self.fix()
        self.take_res()

    def check_enter(self):
        self.login_value = self.lineEdit.text()
        client_socket.send(bytes(self.login_value, "utf8"))
        self.password_value = self.lineEdit_2.text()
        client_socket.send(bytes(self.password_value, "utf8"))
        self.take_res()
        # self.authorize()

    def fix(self):
        self.lineEdit.setText("yo")
        client_socket.send(bytes(self.lineEdit.text(), "utf8"))
        self.lineEdit.setText("")

    def open_chat_page(self):
        w3.show()
        w1.hide()

    def take_res(self):
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == 'go_open_chat_page':
            self.open_chat_page()


class RegWindow(QtWidgets.QMainWindow, Registration_page.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.register)

    def register(self):
        self.login_value = self.lineEdit.text()
        self.password_value = self.lineEdit_2.text()
        self.password_value_again = self.lineEdit_3.text()
        if self.password_value == self.password_value_again:
            client_socket.send(bytes(self.login_value, "utf8"))
            client_socket.send(bytes(self.password_value, "utf8"))
            # self.sending()
            self.take_ress()

    def to_enter_page(self):
        w.show()
        w2.hide()

    def take_ress(self):
        msg = client_socket.recv(BUFSIZ).decode("utf8")
        if msg == 'go_open_start_page':
            self.to_enter_page()


class ChatWindow(QtWidgets.QMainWindow, New_chat_3.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.receive)
        self.pushButton.clicked.connect(self.send)

    def receive(self):
        while True:
            try:
                msg = client_socket.recv(BUFSIZ).decode("utf8")
                self.textEdit.append(msg)
                break
            except OSError:
                break

    def send(self):
        msg = self.textEdit_2.toPlainText()
        self.textEdit_2.clear()
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.close()


HOST = '85.143.66.44'
PORT = 80

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)


def on_closing(event=None):
    client_socket.send("{quit}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w1 = EnterWindow()
    w2 = RegWindow()
    w = StartWindow()
    w3 = ChatWindow()
    w.show()
    sys.exit(app.exec_())
