import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ImageUtils


class CoolWindow(QMainWindow):

    def __init__(self):
        super(CoolWindow, self).__init__(flags=None)

        self.orig_image = None
        self.processed_image = None

        self.setGeometry(50, 50, 950, 500)
        self.setWindowTitle('pRo ImAgE eDiToR')
        # self.setWindowIcon(QIcon('logo.png'))

        # Label for fileMenu object Open
        self.openAction = QAction('&Open File', self)
        self.openAction.setShortcut('Ctrl+O')
        self.openAction.setStatusTip('Open file from disk.')
        self.openAction.triggered.connect(self.file_open_clicked)

        # Label for fileMenu object Save
        self.saveAction = QAction('&Save File', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save file to disk.')
        self.saveAction.triggered.connect(self.file_save_clicked)

        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit program.')
        self.exitAction.triggered.connect(self.close_application_clicked)

        # Label for editMenu object Grayscale
        self.grayScaleAction = QAction('&Grayscale', self)
        self.grayScaleAction.setShortcut('Ctrl+G')
        self.grayScaleAction.setStatusTip('Convert currently selected image to grayscale.')
        # TODO: replace w/ compute and display grayscale function call
        self.grayScaleAction.triggered.connect(self.grayscale_clicked)


        # Label for editMenu object Grayscale
        self.binarizeAction = QAction('&Binarize', self)
        self.binarizeAction.setShortcut('Ctrl+B')
        self.binarizeAction.setStatusTip('Biarize currently selected image using selected thresholds.')
        # TODO: replace w/ compute and display binarize function call
        self.binarizeAction.triggered.connect(self.binarize_clicked)

        # Label for helpMenu object About
        self.helpAction = QAction('&About', self)
        self.helpAction.setShortcut('Ctrl+H')
        self.helpAction.setStatusTip('Show information about the program.')
        # replace w/ display About pop-up function call
        self.helpAction.triggered.connect(self.help_about_clicked)

        self.statusBar = self.statusBar()

        # Menu bar definition
        self.mainMenu = self.menuBar()

        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.mainMenu.addMenu('&Edit')
        self.editMenu.addAction(self.grayScaleAction)
        self.editMenu.addAction(self.binarizeAction)

        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.helpAction)

        self.windowCentralWidget = QWidget()
        self.setCentralWidget(self.windowCentralWidget)
        self.imagesLayout = QHBoxLayout()
        self.centralWidget().setLayout(self.imagesLayout)

        self.home()

    def grayscale_clicked(self):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'You\'re an idiot')
            return

        self.processed_image = ImageUtils.rgb2grayscale(self.orig_image)
        self.afterImgLabel.update()

    def binarize_clicked(self):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'You\'re an idiot')
            return

    def home(self):
        # btn = QPushButton('Quit', self)
        # btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        # btn.setGeometry(860, 440, 60, 40)

        # Toolbar Label for Grayscale
        grayAction = QAction(QtGui.QIcon('grayscale.jpg'), 'Convert currently selected image to grayscale.', self)
        grayAction.triggered.connect(self.grayscale_clicked)

        # Toolbar Label for Binarize
        binarizeAction = QAction(QtGui.QIcon('binarize.png'), 'Convert currently selected image to binarized image.',
                                 self)
        binarizeAction.triggered.connect(self.binarize_clicked)

        # Toolbar definition
        self.toolBar = QToolBar('Edit Options')
        self.toolBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.addAction(grayAction)
        self.toolBar.addAction(binarizeAction)

        self.show()

    def close_application_clicked(self):
        choice = QMessageBox.question(self, 'Quit Program?',
                                      'Are you sure you want to close the program? Unsaved changes may be lost.',
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('Closing program.')
            sys.exit()
        else:
            pass
        print('Application closed.')

    def help_about_clicked(self):
        QMessageBox.information(self, 'About', 'String cu despre program si plm.')

    def file_open_clicked(self):
        filePath, selectedFilter = QFileDialog.getOpenFileName(self, 'Open Image', '',
                                               'Image Files (*.png; *.jpg; *.bmp; *.gif; *.jpeg; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')
        if not filePath:
            return

        self.orig_image = QImage()
        self.processed_image = QImage()

        self.orig_image.load(filePath)
        self.processed_image.load(filePath)

        self.init_images_layout()

        self.beforeImgLabel.update()
        self.afterImgLabel.update()

        return filePath

    def file_save_clicked(self):
        if self.processed_image is None:
            QMessageBox.critical(self, 'Error', 'You\'re an idiot')
            return

        filePath, selectedFilter = QFileDialog.getSaveFileName(self, 'Save File',
                                                               'untitled.png',
                                                               'PNG (*.png);;BMP (*.bmp);;JPEG (*.jpg *.jpeg);;\
                                                               GIF (*.gif);;PBM (*.pbm);;PGm (*.pgb);;PPM (*.ppm);;\
                                                               XBM (*.xbm);;XPM(*.xpm)')
        if not filePath:
            return

        self.processed_image.save(filePath)

    def init_images_layout(self): # TODO: implement scaling math and maybe tidy it up a bit
        self.beforeImgPixMap = QPixmap(self.orig_image)
        self.beforeImgLabel = QLabel()
        self.beforeImgLabel.resize(500, 500)
        self.beforeImgLabel.setPixmap(self.beforeImgPixMap.scaledToHeight(self.beforeImgLabel.height()))
        self.imagesLayout.addWidget(self.beforeImgLabel)

        self.afterImgPixMap = QPixmap(self.processed_image)
        self.afterImgLabel = QLabel()
        self.afterImgLabel.resize(500, 500)
        self.afterImgLabel.setPixmap(self.afterImgPixMap.scaledToHeight(self.afterImgLabel.height()))
        self.imagesLayout.addWidget(self.afterImgLabel)
