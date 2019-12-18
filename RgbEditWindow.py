from threading import Timer
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class RgbEditWindow(QWidget):

    timeOut = 250  # ms

    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle(title)

        self.rVal = 0
        self.gVal = 0
        self.bVal = 0

        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)

        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)

        self.rValSlider = QSlider()
        self.gValSlider = QSlider()
        self.bValSlider = QSlider()

        self.rValSlider.valueChanged.connect(self.rValSliderChangeValue)
        self.gValSlider.valueChanged.connect(self.gValSliderChangeValue)
        self.bValSlider.valueChanged.connect(self.bValSliderChangeValue)

        self.rValSlider.setMinimum(-255)
        self.rValSlider.setMaximum(255)

        self.gValSlider.setMinimum(-255)
        self.gValSlider.setMaximum(255)

        self.bValSlider.setMinimum(-255)
        self.bValSlider.setMaximum(255)

        self.rValSliderLabel = QLabel(str(self.rVal))
        self.gValSliderLabel = QLabel(str(self.gVal))
        self.bValSliderLabel = QLabel(str(self.bVal))

        self.leftColumn = QWidget()
        self.leftColumn.setLayout(QVBoxLayout())
        self.leftColumn.layout().addWidget(QLabel('Red'))
        self.leftColumn.layout().addWidget(self.rValSlider)
        self.leftColumn.layout().addWidget(self.rValSliderLabel)

        self.middleColumn = QWidget()
        self.middleColumn.setLayout(QVBoxLayout())
        self.middleColumn.layout().addWidget(QLabel('Green'))
        self.middleColumn.layout().addWidget(self.gValSlider)
        self.middleColumn.layout().addWidget(self.gValSliderLabel)

        self.rightColumn = QWidget()
        self.rightColumn.setLayout(QVBoxLayout())
        self.rightColumn.layout().addWidget(QLabel('Blue'))
        self.rightColumn.layout().addWidget(self.bValSlider)
        self.rightColumn.layout().addWidget(self.bValSliderLabel)

        self.mainLayout.addWidget(self.leftColumn)
        self.mainLayout.addWidget(self.middleColumn)
        self.mainLayout.addWidget(self.rightColumn)

    def showEvent(self, QShowEvent):
        # reset sliders
        print('rgb edit window visible')
        self.rValSliderChangeValue(self.rVal, True)
        self.gValSliderChangeValue(self.gVal, True)
        self.bValSliderChangeValue(self.bVal, True)

    def rValSliderChangeValue(self, value, force=False):
        self.rVal = value

        self.rValSliderLabel.setText(str(self.rVal))
        print('rVal new value:{}'.format(self.rVal))
        self.resetTimer()

    def gValSliderChangeValue(self, value, force=False):
        self.gVal = value

        self.gValSliderLabel.setText(str(self.gVal))
        print('gVal new value:{}'.format(self.gVal))
        self.resetTimer()

    def bValSliderChangeValue(self, value, force=False):
        self.bVal = value

        self.bValSliderLabel.setText(str(self.bVal))
        print('bVal new value:{}'.format(self.bVal))
        self.resetTimer()

    def timerCallback(self):
        pass

    def resetTimer(self):
        print('resetTimer called')
        self.updateTimer.cancel()
        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)
        self.updateTimer.start()

    def getSliderValues(self):
        return self.rVal, self.gVal, self.bVal
