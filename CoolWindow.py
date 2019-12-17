import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ImageUtils

class CoolWindow(QMainWindow):

    def __init__(self):
        super(CoolWindow, self).__init__()

        self.orig_image = None
        self.processed_image = None

        self.setGeometry(50, 50, 950, 500)
        self.setWindowTitle("pRo ImAgE eDiToR")
        # self.setWindowIcon(QIcon('logo.png'))

        # Label for fileMenu object Open
        openAction = QAction("&Open File", self)
        openAction.setShortcut("Ctrl+O")
        openAction.setStatusTip('Open file from disk.')
        openAction.triggered.connect(self.file_open_clicked)

        # Label for fileMenu object Save
        saveAction = QAction("&Save File", self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setStatusTip('Save file to disk.')
        saveAction.triggered.connect(self.file_save_clicked)

        exitAction = QAction("&Exit", self)
        exitAction.setShortcut("Ctrl+Q")
        exitAction.setStatusTip('Exit program.')
        exitAction.triggered.connect(self.close_application_clicked)

        # Label for editMenu object Grayscale
        grayScaleAction = QAction("&Grayscale", self)
        grayScaleAction.setShortcut("Ctrl+G")
        grayScaleAction.setStatusTip('Convert currently selected image to grayscale.')
        # TODO: replace w/ compute and display grayscale function call
        grayScaleAction.triggered.connect(self.grayscale_clicked)


        # Label for editMenu object Grayscale
        binarizeAction = QAction("&Binarize", self)
        binarizeAction.setShortcut("Ctrl+B")
        binarizeAction.setStatusTip('Biarize currently selected image using selected thresholds.')
        # TODO: replace w/ compute and display binarize function call
        binarizeAction.triggered.connect(self.binarize_clicked)

        # Label for helpMenu object About
        helpAction = QAction("&About", self)
        helpAction.setShortcut("Ctrl+H")
        helpAction.setStatusTip('Show information about the program.')
        # replace w/ display About pop-up function call
        helpAction.triggered.connect(self.help_about_clicked)

        statusBar = self.statusBar()

        # Menu bar definition
        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        editMenu = mainMenu.addMenu('&Edit')
        editMenu.addAction(grayScaleAction)
        editMenu.addAction(binarizeAction)

        helpMenu = mainMenu.addMenu('&Help')
        helpMenu.addAction(helpAction)

        self.home()

    def grayscale_clicked(self):
        if self.orig_image is None:
            prompt = QMessageBox.critical(self, 'Error', 'You\'re an idiot')

    def binarize_clicked(self):
        if self.orig_image is None:
            prompt = QMessageBox.critical(self, 'Error', 'You\'re an idiot')

    def home(self):
        btn = QPushButton("Quit", self)
        btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        btn.resize(60, 40)
        btn.move(860, 440)

        # Toolbar Label for Grayscale
        grayAction = QAction(QtGui.QIcon('grayscale.jpg'), 'Convert currently selected image to grayscale.', self)
        grayAction.triggered.connect(self.close_application_clicked)

        # Toolbar Label for Binarize
        binarizeAction = QAction(QtGui.QIcon('binarize.png'), 'Convert currently selected image to binarized image.',
                                 self)
        binarizeAction.triggered.connect(self.close_application_clicked)

        # Toolbar defintion
        self.toolBar = self.addToolBar("Edit Options")
        self.toolBar.addAction(grayAction)
        self.toolBar.addAction(binarizeAction)

        self.show()

    def close_application_clicked(self):
        choice = QMessageBox.question(self, 'Quit Program?',
                                      "Are you sure you want to close the program? Unsaved changes may be lost.",
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print("Closing program.")
            sys.exit()
        else:
            pass
        print("Application closed.")

    def help_about_clicked(self):
        prompt = QMessageBox.information(self, 'About', "String cu despre program si plm.")

    def file_open_clicked(self):
        filePath = QFileDialog.getOpenFileName(self, 'Open Image', "",
                                               'Image Files (*.png; *.jpg; *.bmp; *.gif; *.jpeg; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')
        self.orig_image = QImage(filePath)
        self.processed_image = self.orig_image
        return filePath

    def file_save_clicked(self):
        filePath = QFileDialog.getSaveFileName(self, 'Save File')
        self.processed_image.save(filePath)
