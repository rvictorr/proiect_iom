from threading import Timer
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from src.TextSlider import TextSlider


class RgbEditWindow(QWidget):

    timeOut = 250  # ms

    def __init__(self, parent, title):
        super().__init__(parent, QtCore.Qt.Tool)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle(title)

        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)

        self.setLayout(QHBoxLayout())

        def sliderValueChangedCallback(value):
            if value > 255:
                value = 255
            if value < -255:
                value = -255
            self.resetTimer()
            return value

        self.rSlider = TextSlider(self, 'Red', -255, 255, 0)
        self.rSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.gSlider = TextSlider(self, 'Green', -255, 255, 0)
        self.gSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.bSlider = TextSlider(self, 'Blue', -255, 255, 0)
        self.bSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.layout().addWidget(self.rSlider)
        self.layout().addWidget(self.gSlider)
        self.layout().addWidget(self.bSlider)

    def reset(self):
        self.rSlider.reset()
        self.gSlider.reset()
        self.bSlider.reset()

    def timerCallback(self):
        pass

    def resetTimer(self):
        # print('resetTimer called')
        self.updateTimer.cancel()
        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)
        self.updateTimer.start()

    def getSliderValues(self):
        return self.rSlider.value(), self.gSlider.value(), self.bSlider.value()

    def showEvent(self, QShowEvent):
        self.activateWindow()