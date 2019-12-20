from PyQt5 import QtCore
from PyQt5.QtWidgets import *


class TextSlider(QWidget):

    def __init__(self, parent, defaultValue=0):
        super().__init__(parent)

        self.sliderValue = defaultValue
        self.onSliderValueChanged = lambda value: value

        self.setLayout(QVBoxLayout())

        self.slider = QSlider()
        self.slider.valueChanged.connect(self.sliderChangeValue)

        self.label = QLabel()

        self.sliderText = QLineEdit()
        self.sliderText.editingFinished.connect(self.sliderTextEdited)
        self.setSliderTextWidth()
        self.sliderText.setText(str(defaultValue))

        self.layout().addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.layout().addWidget(self.slider, 0, QtCore.Qt.AlignHCenter)
        self.layout().addWidget(self.sliderText, 0, QtCore.Qt.AlignHCenter)

    def value(self):
        return self.slider.value()

    def setSliderPosition(self, pos):
        self.slider.setSliderPosition(pos)

    def setSliderValueChangedCallback(self, func):
        self.onSliderValueChanged = func

    def sliderTextEdited(self):
        text = self.sliderText.text()
        self.sliderChangeValue(int(text))
        self.setSliderPosition(self.sliderValue)

    def sliderChangeValue(self, value, force=False):
        # call function
        self.sliderValue = self.onSliderValueChanged(value=value)  # should probably use a QValidator for this

        if force:
            self.slider.setSliderPosition(value)

        self.sliderText.setText(str(self.sliderValue))
        # print('New {} slider value:{}'.format(self.label.text(), self.slider.value()))

    def setSliderTextWidth(self):
        fm = self.sliderText.fontMetrics()
        w = fm.boundingRect('999').width()
        self.sliderText.setFixedWidth(w+8)  # +8 for horizontal margins

    def setLabelText(self, text):
        self.label.setText(text)

    def setSliderLimits(self, min, max):
        self.slider.setMinimum(min)
        self.slider.setMaximum(max)

    def showEvent(self, QShowEvent):
        self.sliderChangeValue(self.sliderValue, True)