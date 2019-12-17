import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 950, 500)
        self.setWindowTitle("pRo ImAgE eDiToR")
        #self.setWindowIcon(QIcon('logo.png'))

        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.statusBar()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')


        self.home()


    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(60, 40)
        btn.move(860, 440)
        self.show()

    def close_application(self):
        print("whooaaaa so custom!!!")
        sys.exit()



        '''
        # File Browser
        openFile = QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        '''

        # fileMenu.addAction(file_open)

# Function to run App
def run():
    app = QApplication([])
    GUI = Window()
    app.exec()

run()



