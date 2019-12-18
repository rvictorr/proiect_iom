from multiprocessing.pool import ThreadPool
from threading import Timer
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import ImageUtils
from BinarizationWindow import BinarizationWindow
from AspectRatioPixmapLabel import AspectRatioPixmapLabel


class CoolWindow(QMainWindow):

    def __init__(self):
        super(CoolWindow, self).__init__()

        self.pool = ThreadPool(processes=1)
        self.orig_image = None
        self.processed_image = None

        self.beforeImgPixMap = QPixmap()
        self.beforeImgLabel = AspectRatioPixmapLabel()
        self.afterImgPixMap = QPixmap()
        self.afterImgLabel = AspectRatioPixmapLabel()

        self.binarizationWindow = BinarizationWindow(self, 'Binarize')

        self.width = QApplication.desktop().screenGeometry().width() // 3
        self.height = QApplication.desktop().screenGeometry().height() // 3
        self.setGeometry(QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            QtCore.QSize(self.width, self.height),
            QApplication.desktop().screenGeometry()
        ))
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
        self.exitAction.triggered.connect(self.close)

        # Label for editMenu object Grayscale
        self.grayScaleAction = QAction('&Grayscale', self)
        self.grayScaleAction.setShortcut('Ctrl+G')
        self.grayScaleAction.setStatusTip('Convert currently selected image to grayscale.')
        self.grayScaleAction.triggered.connect(self.grayscale_clicked)


        # Label for editMenu object Grayscale
        self.binarizeAction = QAction('&Binarize', self)
        self.binarizeAction.setShortcut('Ctrl+B')
        self.binarizeAction.setStatusTip('Binarize currently selected image using selected thresholds.')
        # TODO: replace w/ compute and display binarize function call
        self.binarizeAction.triggered.connect(lambda: self.binarize_clicked(QtGui.QCursor.pos()))

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

        self.windowCentralWidget = QSplitter()  # TODO: maybe disable dragging?
        self.setCentralWidget(self.windowCentralWidget)
        self.centralWidget().addWidget(self.beforeImgLabel)
        self.centralWidget().addWidget(self.afterImgLabel)

        self.home()

    def grayscale_clicked(self):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'You\'re an idiot')
            return

        def thread_func():
            self.processed_image = ImageUtils.rgb2grayscale(self.orig_image)
            # TODO: fix bug with opening files from desktop
            self.update_after_image()

        self.pool.apply_async(thread_func)

    def binarize_clicked(self, pos):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'You\'re an idiot')
            return

        print('binarization click pos: {}'.format(pos))
        self.binarizationWindow.move(pos)
        self.binarizationWindow.show()

        def thread_func():
            def onUpdate():
                print('binarization onUpdate called')
                thr1, thr2 = self.binarizationWindow.getThresholds()
                self.processed_image = ImageUtils.binarize(self.orig_image, thr1, thr2)
                self.update_after_image()

            self.binarizationWindow.timerCallback = onUpdate
            self.binarizationWindow.resetTimer()  # needed because we changed timerCallback

        self.pool.apply_async(thread_func)

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
        binarizeAction.triggered.connect(lambda: self.binarize_clicked(QtGui.QCursor.pos()))

        # Toolbar definition
        self.toolBar = QToolBar('Edit Options')
        self.toolBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.addAction(grayAction)
        self.toolBar.addAction(binarizeAction)

        self.show()

    def closeEvent(self, event):
        print('close event')
        if not self.show_close_program_prompt():
            event.ignore()
            return

        self.pool.close()
        self.pool.join()
        event.accept()

    def show_close_program_prompt(self):
        choice = QMessageBox.question(self, 'Quit Program?',
                                      'Are you sure you want to close the program? Unsaved changes may be lost.',
                                      QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            print('Closing program.')
            return True

        return False

    def help_about_clicked(self):
        QMessageBox.information(self, 'About', 'String cu despre program si plm.')

    def file_open_clicked(self):
        filePath, selectedFilter = QFileDialog.getOpenFileName(self, 'Open Image', '',
                                               'Image Files (*.png; *.jpg; *.bmp; *.gif; *.jpeg; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')
        if not filePath:
            return

        def thread_func():  # really janky code but it works if you're careful with it (we should use locks n shit)
            if self.orig_image is None:
                self.orig_image = QImage()
                self.processed_image = QImage()

            self.orig_image.load(filePath)
            self.processed_image.load(filePath)

            self.update_before_image()
            self.update_after_image()

            self.beforeImgLabel.update()
            self.afterImgLabel.update()
            print('Finished opening image')

        self.pool.apply_async(thread_func)

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

        def thread_func():
            self.processed_image.save(filePath)
            print('Finished saving image')

        self.pool.apply_async(thread_func)

    def update_before_image(self):
        self.beforeImgPixMap.convertFromImage(self.orig_image)
        self.beforeImgLabel.setPixmap(self.beforeImgPixMap)
        self.beforeImgLabel.update()

    def update_after_image(self):
        self.afterImgPixMap.convertFromImage(self.processed_image)
        self.afterImgLabel.setPixmap(self.afterImgPixMap)
        self.afterImgLabel.update()