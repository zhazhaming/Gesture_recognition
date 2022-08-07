import threading

from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread, QSize

import sys

# from manager import *  # 2022.1.27 manger 可以暂时删去，不影响跑项目
from MeetingWindow import MeetingWindow
from StatusBarWindow import *
from model import feapoint_demo


# from multiprocessing import Manager
# from gui.MeetingWindow import MeetingWindow

# 这是初始界面
# 界面里选择是创建会议，还是加入会议
from server.SocketServer import SocketServer

from virtual_mouse.demo_windows import VirtualMouse



class InitWindow(QWidget):
    def __init__(self, mainWindow):
        QWidget.__init__(self)
        self.mainWindow = mainWindow
        mainWindow.setWindowTitle('主界面')
        mainWindow.setWindowIcon(QIcon('Qt.ico'))
        mainWindow.setFixedSize(QSize(600, 600))
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./gui/picture/main_win.png")))
        mainWindow.setPalette(palette)
        layout = QVBoxLayout()
        createButton = QPushButton("Gesture control")
        createButton.clicked.connect(self.createMeeting)
        layout.addWidget(createButton)

        createButton_2 = QPushButton("Mouse control")
        createButton_2.clicked.connect(lambda:self.create_mouse())
        # layout = QVBoxLayout()
        layout.addWidget(createButton_2)

        # joinButton = QPushButton("加入会议")
        # joinButton.clicked.connect(self.joinMeeting)
        # hLayout = QHBoxLayout()
        # lineEdit = QLineEdit()
        # self.lineEdit = lineEdit
        # hLayout.addWidget(lineEdit)
        # hLayout.addWidget(joinButton)

        # layout.addLayout(hLayout)

        self.setLayout(layout)

    def joinMeeting(self):
        self.mainWindow.manager.joinMeeting(self.lineEdit.text())
        self.mainWindow.setCentralWidget(MeetingWindow(self.mainWindow))

    def createMeeting(self):
        statusBarWindow = StatusBarWindow()
        statusBarWindow.show()
        self.mainWindow.childWindows['statusBarWindow'] = statusBarWindow
        socket_server = SocketServer()

        def socket_server_start():
            gestureListener = GestureListener(statusBarWindow)
            socket_server.runServer(gestureListener)

        def socket_client_start():
            client = feapoint_demo.GestureRecognize()
            client.main()


        self.mainWindow.closeEvents.append(socket_server.terminateServer)
        thread1 = threading.Thread(target=socket_server_start)
        # thread2 = threading.Threa
        # d(target=socket_client_start)
        thread1.start()
        # thread2.start()
        self.mainWindow.setCentralWidget(MeetingWindow(self.mainWindow))
        self.mainWindow.setHidden(True)
        gestureRecognize = feapoint_demo.GestureRecognize()
        # if gestureRecognize.startUpClient(socketConfig.IP, socketConfig.PORT):
        if gestureRecognize.startUpClient():
            gestureRecognize.main()
            # gestureRecognize.gettt()  # 接口 返回手势
        # print(111)


    def create_mouse(self):
        self.mainWindow.setCentralWidget(MeetingWindow(self.mainWindow))
        self.mainWindow.setHidden(True)

        control = VirtualMouse()
        control.recognize()
        # print(222)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QMainWindow()
    # win.manager = Manager()
    win.setCentralWidget(InitWindow(win))
    win.show()
    app.exec_()
