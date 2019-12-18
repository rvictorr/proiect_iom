from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel


class AspectRatioPixmapLabel(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.pix = None
        self.setMinimumSize(1, 1)
        self.setScaledContents(False)

    def setPixmap(self, p):
        self.pix = p
        super().setPixmap(self.scaledPixMap())

    def sizeHint(self):
        w = self.width()
        return QtCore.QSize(w, self.heightForWidth(w))

    def scaledPixMap(self):
        return self.pix.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    def resizeEvent(self, *args, **kwargs):
        if self.pix is not None:
            super().setPixmap(self.scaledPixMap())

    def heightForWidth(self, width):
        return self.height() if self.pix is None else self.pix.height()*width/self.pix.width()
