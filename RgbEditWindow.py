from threading import Timer
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from TextSlider import TextSlider


class RgbEditWindow(QWidget):

    timeOut = 250  # ms

    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle(title)

        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)

        self.setLayout(QHBoxLayout(self))

        def sliderValueChangedCallback(value):
            if value > 255:
                value = 255
            if value < -255:
                value = -255
            self.resetTimer()
            return value

        self.rSlider = TextSlider(self, -255, 255, 0)
        self.rSlider.setLabelText('Red')
        self.rSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.gSlider = TextSlider(self, -255, -255, 0)
        self.gSlider.setLabelText('Green')
        self.gSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.bSlider = TextSlider(self, -255, -255, 0)
        self.bSlider.setLabelText('Blue')
        self.bSlider.setSliderValueChangedCallback(sliderValueChangedCallback)

        self.layout().addWidget(self.rSlider)
        self.layout().addWidget(self.gSlider)
        self.layout().addWidget(self.bSlider)

    def timerCallback(self):
        pass

    def resetTimer(self):
        # print('resetTimer called')
        self.updateTimer.cancel()
        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)
        self.updateTimer.start()

    def getSliderValues(self):
        return self.rSlider.value(), self.gSlider.value(), self.bSlider.value()
