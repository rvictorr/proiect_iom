from PyQt5.QtWidgets import QApplication
from CoolWindow import CoolWindow

# Function to run App
def run():
    app = QApplication([])
    GUI = CoolWindow()
    app.exec()

    pass
    # VICTOR
    """
    app = QApplication([])
    window = QWidget()
    window.setGeometry(500, 500, 1000, 1000)
    imagesLayout = QHBoxLayout()
    window.setLayout(imagesLayout)
    window.show()

    image = QImage()
    image.load('test.jpg')
    # image.load('gradient.png')
    # image.load('gradient_small.png')
    # image.load('dot.png')

    grayscaleImg = ImageUtils.rgb2grayscale(image)
    binImg = ImageUtils.binarize(image, 70, 170)

    grayscaleImg.save('grayscale.jpg', None, 100)
    binImg.save('binarized.jpg', None, 100)

    pixMap = QPixmap(grayscaleImg)
    beforeImg = QLabel()
    beforeImg.resize(500, 500)
    beforeImg.setPixmap(pixMap.scaledToHeight(beforeImg.height()))
    imagesLayout.addWidget(beforeImg)

    pixMap = QPixmap(binImg)
    afterImg = QLabel()
    afterImg.resize(500, 500)
    afterImg.setPixmap(pixMap.scaledToHeight(afterImg.height()))
    imagesLayout.addWidget(afterImg)
    # window.resize(500, 500)
    """

run()



