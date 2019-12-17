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
        openAction = QAction("&Open File", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open file from disk.')
        openAction.triggered.connect(self.file_open)

        # Label for fileMenu object Save
        saveAction = QAction("&Save File", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save file to disk.')
        saveAction.triggered.connect(self.close_application)

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
        helpAction.triggered.connect(self.help_about)

        self.statusBar()

        # Menu bar definition
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)

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
        choice = QMessageBox.question(self, 'Quit Program?',
                                            "Are you sure you want to close the program? Unsaved changes may be lost.",
                                            QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Closing program.")
            sys.exit()
        else:
            pass
        print("Application closed.")

    def help_about(self):
        prompt = QMessageBox.information(self, 'About', "String cu despre program si plm.")

    def file_open(self):
        fileName = QFileDialog.getOpenFileName(self, 'Open Image', "", 'Image Files (*.png; *.jpg; *.bmp; *.gif; *.jpeg; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')
        return fileName






# Function to run App
def run():
    app = QApplication([])
    GUI = Window()
    app.exec()

run()



