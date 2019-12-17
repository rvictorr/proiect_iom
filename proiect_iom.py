import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 950, 500)
        self.setWindowTitle("pRo ImAgE eDiToR")
        #self.setWindowIcon(QIcon('logo.png'))

        # Label for fileMenu object Open
        extractAction = QAction("&Open", self)
        extractAction.setShortcut("Ctrl+O")
        extractAction.setStatusTip('Open file from disk.')
        extractAction.triggered.connect(self.close_application)

        # Label for editMenu object Grayscale
        editAction0 = QAction("&Grayscale", self)
        editAction0.setShortcut("Ctrl+G")
        editAction0.setStatusTip('Convert currently selected image to grayscale.')
        # replace w/ compute and display grayscale function call
        editAction0.triggered.connect(self.close_application)

        # Label for editMenu object Grayscale
        editAction1 = QAction("&Binarize", self)
        editAction1.setShortcut("Ctrl+B")
        editAction1.setStatusTip('Biarize currently selected image using selected thresholds.')
        # replace w/ compute and display binarize function call
        editAction1.triggered.connect(self.close_application)

        # Label for helpMenu object About
        helpAction = QAction("&About", self)
        helpAction.setShortcut("Ctrl+H")
        helpAction.setStatusTip('Show information about the program.')
        # replace w/ display About pop-up function call
        helpAction.triggered.connect(self.close_application)

        self.statusBar()

        # Menu bar definition
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)

        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(editAction0)
        editMenu.addAction(editAction1)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)

        self.home()


    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(60, 40)
        btn.move(860, 440)

        # Toolbar Label for Grayscale
        grayAction = QAction(QtGui.QIcon('grayscale.jpg'), 'Convert currently selected image to grayscale.', self)
        grayAction.triggered.connect(self.close_application)

        # Toolbar Label for Binarize
        binarizeAction = QAction(QtGui.QIcon('binarize.png'), 'Convert currently selected image to binarized image.', self)
        binarizeAction.triggered.connect(self.close_application)

        # Toolbar defintion
        self.toolBar = self.addToolBar("Edit Options")
        self.toolBar.addAction(grayAction)
        self.toolBar.addAction(binarizeAction)

        self.show()

    def close_application(self):
        choice = QtGui.QMessageBox.question(self, 'Extract!',
                                            "Get into the chopper?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Extracting Naaaaaaoooww!!!!")
            sys.exit()
        else:
            pass

        print("Application closed.")
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



