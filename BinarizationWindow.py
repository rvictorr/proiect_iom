from threading import Timer
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from TextSlider import TextSlider


class BinarizationWindow(QWidget):

    timeOut = 250  # ms

    def __init__(self, parent, title):
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle(title)

        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)

        self.setLayout(QHBoxLayout())

        self.textSlider1 = TextSlider(self, 127)
        self.textSlider1.setLabelText('Threshold 1')
        self.textSlider1.setSliderLimits(0, 255)

        def slider1ValueChangedCallback(value):
            if value > self.textSlider2.value():
                # value = self.textSlider1.value()
                self.textSlider2.setSliderPosition(value)
            self.resetTimer()
            return value

        self.textSlider1.setSliderValueChangedCallback(slider1ValueChangedCallback)

        self.textSlider2 = TextSlider(self, 127)
        self.textSlider2.setLabelText('Threshold 2')
        self.textSlider2.setSliderLimits(0, 255)

        def slider2ValueChangedCallback(value):
            if value < self.textSlider1.value():
                value = self.textSlider1.value()
                self.textSlider2.setSliderPosition(value)
            self.resetTimer()
            return value

        self.textSlider2.setSliderValueChangedCallback(slider2ValueChangedCallback)

        self.layout().addWidget(self.textSlider1)
        self.layout().addWidget(self.textSlider2)

    def timerCallback(self):
        pass

    def resetTimer(self):
        print('resetTimer called')
        self.updateTimer.cancel()
        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)
        self.updateTimer.start()

    def getSliderValues(self):
        return self.textSlider1.value(), self.textSlider2.value()
