from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThreadPool
import ImageUtils
from Worker import Worker
from BinarizationWindow import BinarizationWindow
from RgbEditWindow import RgbEditWindow
from AspectRatioPixmapLabel import AspectRatioPixmapLabel


class CoolWindow(QMainWindow):

    def __init__(self):
        super(CoolWindow, self).__init__()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.orig_image = None
        self.processed_image = None

        self.toolBar = None

        self.beforeImgPixMap = QPixmap()
        self.beforeImgLabel = AspectRatioPixmapLabel(self)
        self.afterImgPixMap = QPixmap()
        self.afterImgLabel = AspectRatioPixmapLabel(self)

        self.binarizationWindow = BinarizationWindow(self, 'Binarize')
        self.rgbEditWindow = RgbEditWindow(self, 'RGB Edit')

        self.width = QApplication.desktop().screenGeometry().width() // 2
        self.height = QApplication.desktop().screenGeometry().height() // 2
        self.setGeometry(QStyle.alignedRect(
            QtCore.Qt.LeftToRight,
            QtCore.Qt.AlignCenter,
            QtCore.QSize(self.width, self.height),
            QApplication.desktop().screenGeometry()
        ))
        self.setWindowTitle('GIE Pro v0.8 (Ghetto Image Editor)')
        self.setWindowIcon(QIcon('icons/ico_logo.png'))

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
        self.saveAction.setEnabled(False)

        # Label for fileMenu object Exit
        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit program.')
        self.exitAction.triggered.connect(self.close)

        # Label for editMenu object Grayscale
        self.grayScaleAction = QAction('&Grayscale', self)
        self.grayScaleAction.setShortcut('Ctrl+G')
        self.grayScaleAction.setStatusTip('Convert currently selected image to grayscale.')
        self.grayScaleAction.triggered.connect(self.grayscale_clicked)
        self.grayScaleAction.setEnabled(False)

        # Label for editMenu object Binarize
        self.binarizeAction = QAction('&Binarize', self)
        self.binarizeAction.setShortcut('Ctrl+B')
        self.binarizeAction.setStatusTip('Binarize currently selected image using selected thresholds.')
        self.binarizeAction.triggered.connect(lambda: self.binarize_clicked(QtGui.QCursor.pos()))
        self.binarizeAction.setEnabled(False)

        # Label for editMenu object RGB Edit
        self.rgbEditAction = QAction('&RGB Edit', self)
        self.rgbEditAction.setShortcut('Ctrl+R')
        self.rgbEditAction.setStatusTip('Edit the RGB values of the current image.')
        self.rgbEditAction.triggered.connect(lambda: self.rgbEdit_clicked(QtGui.QCursor.pos()))
        self.rgbEditAction.setEnabled(False)

        # Label for helpMenu object About
        self.helpAction = QAction('&About', self)
        self.helpAction.setShortcut('Ctrl+H')
        self.helpAction.setStatusTip('Show information about the program.')
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
        self.editMenu.addAction(self.rgbEditAction)

        self.helpMenu = self.mainMenu.addMenu('&Help')
        self.helpMenu.addAction(self.helpAction)

        self.windowCentralWidget = QSplitter()  # TODO: maybe disable dragging?
        self.setCentralWidget(self.windowCentralWidget)
        self.centralWidget().addWidget(self.beforeImgLabel)
        self.centralWidget().addWidget(self.afterImgLabel)

        self.setupToolbar()

    def setupToolbar(self):
        # btn = QPushButton('Quit', self)
        # btn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        # btn.setGeometry(860, 440, 60, 40)

        openAction = QAction(QtGui.QIcon('icons/ico_open.png'), 'Open', self)
        openAction.triggered.connect(self.file_open_clicked)

        saveAction = QAction(QtGui.QIcon('icons/ico_save.png'), 'Save', self)
        saveAction.triggered.connect(self.file_save_clicked)
        saveAction.setEnabled(False)

        # Toolbar Label for Grayscale
        grayAction = QAction(QtGui.QIcon('icons/ico_grayscale.png'), 'Convert currently selected image to grayscale.', self)
        grayAction.triggered.connect(self.grayscale_clicked)
        grayAction.setEnabled(False)

        # Toolbar Label for Binarize
        binarizeAction = QAction(QtGui.QIcon('icons/ico_binarize.png'),
                                 'Convert currently selected image to binarized image.',
                                 self)
        binarizeAction.triggered.connect(lambda: self.binarize_clicked(QtGui.QCursor.pos()))
        binarizeAction.setEnabled(False)

        # Toolbar Label for RGB Edit
        rgbEditAction = QAction(QtGui.QIcon('icons/ico_rgbEdit.png'),
                                'Edit the RGB values of the currently selected image.',
                                self)
        rgbEditAction.triggered.connect(lambda: self.rgbEdit_clicked(QtGui.QCursor.pos()))
        rgbEditAction.setEnabled(False)

        # Toolbar definition
        self.toolBar = QToolBar('Edit Options', self)
        self.toolBar.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.toolBar.addAction(openAction)
        self.toolBar.addAction(saveAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(grayAction)
        self.toolBar.addAction(binarizeAction)
        self.toolBar.addAction(rgbEditAction)

    def grayscale_clicked(self):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'Something unexpected happened')
            return

        def thread_func(progress_callback, img):
            return ImageUtils.rgb2grayscale(img)

        def result_func(result):
            self.processed_image = result
            # self.processed_image.swap(result)  # TODO this crashes for some reason

        worker = Worker(thread_func, img=self.orig_image)
        worker.signals.result.connect(result_func)
        worker.signals.finished.connect(self.update_after_image)

        self.threadpool.start(worker)

    def binarize_clicked(self, pos):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'Something unexpected happened')
            return

        self.binarizationWindow.move(pos)
        self.binarizationWindow.show()

        def onTimerReset():
            def thread_func(progress_callback, img, sliderValues):
                # print('Binarizing')
                # return ImageUtils.binarize(img, sliderValues[0], sliderValues[1])
                self.processed_image = ImageUtils.binarize(img, sliderValues[0], sliderValues[1])

            def result_func(result):  # for some reason this doesn't get called
                self.processed_image = result

            worker = Worker(thread_func, img=self.orig_image, sliderValues=self.binarizationWindow.getSliderValues())
            # worker.signals.result.connect(result_func)
            worker.signals.finished.connect(self.update_after_image)

            self.threadpool.start(worker)

        self.binarizationWindow.timerCallback = onTimerReset
        self.binarizationWindow.resetTimer()  # needed because we changed timerCallback


        # def thread_func(progress_callback, img, binWindow):
        #     #  TODO: maybe figure out a way to remove the timer stuff from here
        #     def onUpdate():
        #         print('binarization onUpdate called')
        #         thr1, thr2 = binWindow.getSliderValues()
        #         self.processed_image = ImageUtils.binarize(img, thr1, thr2)
        #         # self.processed_image = ImageUtils.rgb2grayscale(img)
        #         self.update_after_image()
        #
        #     self.binarizationWindow.timerCallback = onUpdate
        #     self.binarizationWindow.resetTimer()  # needed because we changed timerCallback
        #
        # worker = Worker(thread_func, img=self.orig_image, binWindow=self.binarizationWindow)
        # # worker.signals.finished.connect(self.update_after_image)
        #
        # self.threadpool.start(worker)

    def rgbEdit_clicked(self, pos):
        if self.orig_image is None:
            QMessageBox.critical(self, 'Error', 'Something unexpected happened')
            return

        self.rgbEditWindow.move(pos)
        self.rgbEditWindow.show()

        def onTimerReset():
            def thread_func(progress_callback, img, sliderValues):
                rVal, gVal, bVal = sliderValues
                self.processed_image = ImageUtils.rgbEdit(img, rVal, gVal, bVal)

            def result_func(result):  # for some reason this doesn't get called
                self.processed_image = result

            worker = Worker(thread_func, img=self.orig_image, sliderValues=self.rgbEditWindow.getSliderValues())
            # worker.signals.result.connect(result_func)
            worker.signals.finished.connect(self.update_after_image)

            self.threadpool.start(worker)

        self.rgbEditWindow.timerCallback = onTimerReset
        self.rgbEditWindow.resetTimer()  # needed because we changed timerCallback

    def closeEvent(self, event):
        # print('close event')
        if not self.show_close_program_prompt():
            event.ignore()
            return

        self.threadpool.waitForDone(1000)
        self.threadpool.clear()
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
        QMessageBox.information(self, 'About', '\n\n        Ghetto Image Editor v.0.8'
                                               ' \n\n\nGhetto Image Editor was developed as a homework project by Rusu Victor, '
                                               'Deleanu Radu and Iovescu Daniel.\n\nThe current distributin of the program supports image'
                                               ' import and save, grayscale edit, binarization with two threshold levels and RGB edit.')

    def file_open_clicked(self):
        filePath, selectedFilter = QFileDialog.getOpenFileName(self, 'Open Image', '',
                                               'Image Files (*.png; *.jpg; *.bmp; *.gif; *.jpeg; *.pbm; *.pgm; *.ppm; *.xbm; *.xpm)')
        if not filePath:
            return

        if self.orig_image is None:
            self.orig_image = QImage()
            self.processed_image = QImage()

        def thread_func(progress_callback):
            self.orig_image.load(filePath)
            self.processed_image.load(filePath)
            print('Finished opening image')

        def finished_func():
            self.update_before_image()
            self.update_after_image()
            for action in self.toolBar.actions():
                action.setEnabled(True)
            self.saveAction.setEnabled(True)
            self.grayScaleAction.setEnabled(True)
            self.binarizeAction.setEnabled(True)
            self.rgbEditAction.setEnabled(True)

        worker = Worker(thread_func)
        worker.signals.finished.connect(finished_func)

        self.threadpool.start(worker)


    def file_save_clicked(self):
        if self.processed_image is None:
            QMessageBox.critical(self, 'Error', 'Something unexpected happened')
            return

        filePath, selectedFilter = QFileDialog.getSaveFileName(self, 'Save File',
                                                               'untitled.png',
                                                               'PNG (*.png);;BMP (*.bmp);;JPEG (*.jpg *.jpeg);;\
                                                               GIF (*.gif);;PBM (*.pbm);;PGm (*.pgb);;PPM (*.ppm);;\
                                                               XBM (*.xbm);;XPM(*.xpm)')
        if not filePath:
            return

        def thread_func(progress_callback):
            self.processed_image.save(filePath)
            print('Finished saving image')

        worker = Worker(thread_func)

        self.threadpool.start(worker)

    def update_before_image(self):
        self.beforeImgPixMap.convertFromImage(self.orig_image)
        self.beforeImgLabel.setPixmap(self.beforeImgPixMap)
        self.beforeImgLabel.update()

    def update_after_image(self):
        self.afterImgPixMap.convertFromImage(self.processed_image)
        self.afterImgLabel.setPixmap(self.afterImgPixMap)
        self.afterImgLabel.update()
