from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class BinarizationWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)

        self.thr1 = 0
        self.thr2 = 0

        self.mainLayout = QHBoxLayout()
        self.setLayout(self.mainLayout)
        self.thr1Slider = QSlider()
        self.thr2Slider = QSlider()
        self.thr1Slider.valueChanged.connect(self.thr1SliderChangeValue)
        self.thr2Slider.valueChanged.connect(self.thr2SliderChangeValue)
        self.thr1Slider.setMinimum(0)
        self.thr1Slider.setMaximum(255)
        self.thr2Slider.setMinimum(0)
        self.thr2Slider.setMaximum(255)

        self.thr1SliderLabel = QLabel(str(self.thr1))
        self.thr2SliderLabel = QLabel(str(self.thr2))

        self.leftColumn = QWidget()
        self.leftColumn.setLayout(QVBoxLayout())
        self.leftColumn.layout().addWidget(QLabel('Threshold 1'))
        self.leftColumn.layout().addWidget(self.thr1Slider)
        self.leftColumn.layout().addWidget(self.thr1SliderLabel)

        self.rightColumn = QWidget()
        self.rightColumn.setLayout(QVBoxLayout())
        self.rightColumn.layout().addWidget(QLabel('Threshold 2'))
        self.rightColumn.layout().addWidget(self.thr2Slider)
        self.rightColumn.layout().addWidget(self.thr2SliderLabel)

        self.mainLayout.addWidget(self.leftColumn)
        self.mainLayout.addWidget(self.rightColumn)

    def thr1SliderChangeValue(self, value):
        self.thr1 = value

        if value > self.thr2Slider.value():
            self.thr2Slider.setSliderPosition(self.thr1)

        self.thr1SliderLabel.setText(str(self.thr1))
        print('thr1 new value:{}'.format(self.thr1))

    def thr2SliderChangeValue(self, value):
        self.thr2 = value

        if value < self.thr1Slider.value():
            self.thr2Slider.setSliderPosition(self.thr1)
            self.thr2 = self.thr1

        self.thr2SliderLabel.setText(str(self.thr2))
        print('thr2 new value:{}'.format(self.thr2))
