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

        self.setLayout(QVBoxLayout(self))

        self.sliders = QWidget(self)
        self.sliders.setLayout(QHBoxLayout(self))

        self.textSlider1 = TextSlider(self, 'Threshold 1', 0, 255, 127)

        self.textSlider2 = TextSlider(self, 'Threshold 1', 0, 255, 127)

        self.sliders.layout().addWidget(self.textSlider1)
        self.sliders.layout().addWidget(self.textSlider2)

        self.checkBox = QCheckBox('Use 2 thresholds', self)
        self.checkBox.stateChanged.connect(self.checkBoxStateChanged)
        self.checkBoxStateChanged(QtCore.Qt.Unchecked)

        self.layout().addWidget(self.sliders)
        self.layout().addWidget(self.checkBox)

    def reset(self):
        self.textSlider1.reset()
        self.textSlider2.reset()

    def checkBoxStateChanged(self, state):
        if state == QtCore.Qt.Checked:
            def slider1ValueChangedCallback(value):
                if value > self.textSlider2.value():
                    self.textSlider2.setSliderPosition(value)
                self.resetTimer()
                return value

            def slider2ValueChangedCallback(value):
                if value < self.textSlider1.value():
                    value = self.textSlider1.value()
                    self.textSlider2.setSliderPosition(value)
                self.resetTimer()
                return value

            self.textSlider1.setSliderValueChangedCallback(slider1ValueChangedCallback)
            self.textSlider2.setSliderValueChangedCallback(slider2ValueChangedCallback)

        elif state == QtCore.Qt.Unchecked:
            def slider1ValueChangedCallback(value):
                self.textSlider2.setSliderPosition(value)
                self.resetTimer()
                return value

            def slider2ValueChangedCallback(value):
                self.textSlider1.setSliderPosition(value)
                self.resetTimer()
                return value

            self.textSlider1.setSliderValueChangedCallback(slider1ValueChangedCallback)
            self.textSlider2.setSliderValueChangedCallback(slider2ValueChangedCallback)

    def timerCallback(self):
        pass

    def resetTimer(self):
        # print('resetTimer called')
        self.updateTimer.cancel()
        self.updateTimer = Timer(self.timeOut / 1000, self.timerCallback)
        self.updateTimer.start()

    def getSliderValues(self):
        return self.textSlider1.value(), self.textSlider2.value()
