from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class TextSlider(QWidget):

    def __init__(self, parent, labelText='', min=0, max=99, defaultValue=0):
        super().__init__(parent)

        self.defaultValue = defaultValue
        self.sliderValue = self.defaultValue
        self.onSliderValueChanged = lambda value: value

        self.setLayout(QVBoxLayout(self))

        self.slider = QSlider(self)
        self.slider.setRange(min, max)

        self.label = QLabel(self)
        self.label.setText(labelText)

        self.sliderText = QSpinBox(self)
        self.sliderText.setRange(min, max)
        self.reset()

        self.slider.valueChanged.connect(self.sliderChangeValue)
        self.sliderText.valueChanged.connect(self.sliderTextValueChanged)

        self.layout().addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.layout().addWidget(self.slider, 0, QtCore.Qt.AlignHCenter)
        self.layout().addWidget(self.sliderText, 0, QtCore.Qt.AlignHCenter)

    def value(self):
        return self.slider.value()

    def reset(self):
        self.sliderText.setValue(self.defaultValue)

    def setSliderPosition(self, pos):
        self.slider.setSliderPosition(pos)

    def setSliderValueChangedCallback(self, func):
        self.onSliderValueChanged = func

    def sliderTextValueChanged(self, val):
        self.sliderChangeValue(val)
        self.setSliderPosition(self.sliderValue)

    def sliderChangeValue(self, value, force=False):
        self.sliderValue = self.onSliderValueChanged(value=value)  # should probably use a QValidator for this

        if force:
            self.slider.setSliderPosition(value)

        self.sliderText.setValue(self.sliderValue)
        # print('New {} slider value:{}'.format(self.label.text(), self.slider.value()))

    def setRange(self, min, max):
        self.slider.setRange(min, max)
        self.sliderText.setRange(min, max)

    def showEvent(self, QShowEvent):
        self.sliderChangeValue(self.sliderValue, True)