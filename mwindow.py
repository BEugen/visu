import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel
from PyQt5 import QtCore, QtGui

FONT_SIZE = 64

class visuDisp(QWidget):
    def __init__(self, host, port):
        super().__init__()
        self.lb1 = QLabel('1', self)
        self.lb1.setFont(QtGui.QFont("Verdana", FONT_SIZE, QtGui.QFont.Bold))
        self.lb1.setAlignment(QtCore.Qt.AlignHCenter)
        self.lb2 = QLabel('2', self)
        self.lb2.setFont(QtGui.QFont("Verdana", FONT_SIZE, QtGui.QFont.Bold))
        self.lb2.setAlignment(QtCore.Qt.AlignHCenter)
        self.lb3 = QLabel('3', self)
        self.lb3.setFont(QtGui.QFont("Verdana", FONT_SIZE, QtGui.QFont.Bold))
        self.lb3.setAlignment(QtCore.Qt.AlignHCenter)
        self.lb4 = QLabel('4', self)
        self.lb4.setFont(QtGui.QFont("Verdana", FONT_SIZE, QtGui.QFont.Bold))
        self.lb4.setAlignment(QtCore.Qt.AlignHCenter)
        self.initUI(host, port)

    def initUI(self, host, port):
        self.center()
        self.setWindowFlags(QtCore.Qt.Popup)
        self.get_thread = getServerThread(host, port)
        self.connect(self.get_thread, QtCore.pyqtSignal(str, name='dataReceive'), self.dataReceive)
        self.get_thread.start()
        self.show()

    def center(self):
        t = QDesktopWidget().availableGeometry()
        oneline = int((t.height() + t.top())/10)
        self.resize(t.width(), t.height() + t.top())
        self.move(0, 0)
        self.lb1.move(15, oneline*1.5)
        self.lb1.resize(t.width() - 30, oneline)
        self.lb2.move(15, oneline*3.5)
        self.lb2.resize(t.width() - 30, oneline)
        self.lb3.move(15, oneline * 5.5)
        self.lb3.resize(t.width() - 30, oneline)
        self.lb4.move(15, oneline * 7.5)
        self.lb4.resize(t.width() - 30, oneline)

    def dataReceive(self, data):
        self.settext(data[0], data[1], data[2], data[3])

    def settext(self, t1, t2, t3, t4):
        self.lb1.setText("<font color='Red'>" + t1 + "</font>")
        self.lb2.setText("<font color='Red'>" + t2 + "</font>")
        self.lb3.setText("<font color='Red'>" + t3 + "</font>")
        self.lb4.setText("<font color='Red'>" + t4 + "</font>")


class getServerThread(QtCore.QThread):
    def __init__(self, host, port):
        QtCore.QThread.__init__(self)
        self.host = host
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        sock = socket.socket()
        sock.bind((self.host, self.port))
        sock.listen(1)
        conn, addr = sock.accept()
        data = conn.recv(1024)
        if len(data) > 0:
            data_receive = QtCore.pyqtSignal(str, name='dataReceive')
            data_receive.emit(data.decode('utf-8'))

       # for subreddit in self.subreddits:
       #     top_post = self._get_top_post(subreddit)
       #     self.emit(QtCore.SIGNAL('add_post(QString)'), top_post)
       #     self.sleep(2)