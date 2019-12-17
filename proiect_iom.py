from PyQt5.QtWidgets import *
from PyQt5 import QtCore

'''
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))

window.setWindowTitle("Pro Image Edditor")
window.setLayout(layout)
window.show()
'''

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 950, 500)
        self.setWindowTitle("pRo ImAgE EdDiToR")
        #self.setWindowIcon(QIcon('logo.png'))
        self.home()

        '''
        # File Browser
        openFile = QAction("&Open File", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.file_open)
        '''

        # fileMenu.addAction(file_open)

    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(60, 40)
        btn.move(860, 440)
        self.show()


# Function to run App
def run():
    app = QApplication([])
    GUI = Window()
    app.exec()

run()