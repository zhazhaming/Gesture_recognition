"""
! Author：zhazha、hongsen、jiyu
! Date: 2022-03-16

功能：pc端控制、家具控制
作品具有所有权，请勿外传
"""

import os  # 得到当前工作目录  等关于路径等方面的一些操作   https://blog.csdn.net/qq_42026963/article/details/95353469
import sys  # 提供对解释器使用和维护的一些变量的访问，以及与解释器强烈交互的函数   https://blog.csdn.net/qq_38526635/article/details/81739321

from PyQt5.QtWidgets import *  # pyqt是一个视图实现类的model  里面的 Qt*** 基本是对Windows实现的界面的一些操作

# 统一不同工作环境的当前工作目录，统一为项目根目录
current_dir, file_name = os.path.split(os.path.abspath(sys.argv[0]))
print(current_dir)
project_root_dir, dir_name = os.path.split(current_dir)
os.chdir(project_root_dir)
print(os.getcwd())
print(os.getcwd())
# from manager import *  # 这个是import自己的类   会议部分，应该还未启用
from InitWindow import InitWindow  # 这个是import自己的类


# from multiprocessing import Manager
# from gui.MeetingWindow import MeetingWindow
# from gui.InitWindow import InitWindow


class MainWindow(QMainWindow):  # 设置主窗口的尺寸  写一个类，继承QMainWindow，然后初始化与设置一些参数
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(600, 500)  # resize 调整大小   但是调整后却无果？？？
        self.setMinimumSize(600, 500)
        #        self.manager = Manager()        # 因为这个还没启用所以不要也能正常运作
        initWindow = InitWindow(self)
        self.setCentralWidget(initWindow)
        self.childWindows = {}
        self.closeEvents = []

    def closeEvent(self, event):  # closeEvent 关闭事件
        for window in self.childWindows.values():
            window.close()
        for fun in self.closeEvents:
            fun()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication  与初始化窗口，屏幕信息类等相关      sys.argv 传递给Python脚本的命令行参数列表
    QApplication.setStyle(
        QStyleFactory.create('Fusion'))  # 对QApplication设置QStyle样式  Windows有 3种样式 分别Windows windowsvista Fusion
    # 尝试更改视图，无区别
    win = MainWindow()
    win.show()
    app.exec_()
