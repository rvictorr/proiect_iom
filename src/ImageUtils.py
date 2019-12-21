from PyQt5.QtGui import QImage
import numpy as np


def rgb2grayscale(img: QImage):
    width, height = img.width(), img.height()
    img.convertTo(QImage.Format_RGB888, 0)
    ptr = img.constBits()
    realByteCount = img.byteCount()
    calculatedByteCount = width * height * 3
    ptr.setsize(realByteCount)

    slowPath = realByteCount != calculatedByteCount

    imgArray = np.asarray(ptr, dtype=np.uint8)
    mat = [0.2989, 0.5870, 0.1140]

    if slowPath:
        imgArray = imgArray.reshape((height, img.bytesPerLine()))
        grayArr = np.zeros((height, width), dtype=np.uint8)

        for index, line in enumerate(imgArray):
            line = line[:width * 3].reshape(width, 3)
            grayArr[index] = np.dot(line, mat)
    else:
        imgArray = imgArray.reshape((height, width, 3))
        grayArr = np.array(np.dot(imgArray, mat), dtype=np.uint8)

    return QImage(grayArr.data, width, height, img.bytesPerLine()//3, QImage.Format_Grayscale8)


def binarize(img: QImage, thr1, thr2):
    img = rgb2grayscale(img)  # convert it to grayscale first, we don't need RGB
    width, height = img.width(), img.height()

    ptr = img.constBits()
    ptr.setsize(img.byteCount())
    bytesPerPixel = img.byteCount()//(width*height)

    imgArray = np.asarray(ptr, dtype=np.uint8).reshape((height, img.bytesPerLine()//bytesPerPixel, bytesPerPixel))
    condlist = [(imgArray < thr1), np.logical_and(imgArray > thr1, imgArray < thr2), (imgArray > thr2)]
    choicelist = [0, 85, 255]
    bin_arr1 = np.array(np.select(condlist, choicelist), dtype=np.uint8)

    return QImage(bin_arr1.data, bin_arr1.shape[1], bin_arr1.shape[0], img.bytesPerLine(), QImage.Format_Grayscale8)


def rgbEdit(img: QImage, rVal, gVal, bVal):
    width, height = img.width(), img.height()
    img.convertTo(QImage.Format_RGB888, 0)
    ptr = img.constBits()

    realByteCount = img.byteCount()
    calculatedByteCount = width * height * 3
    ptr.setsize(realByteCount)

    slowPath = realByteCount != calculatedByteCount

    imgArray = np.asarray(ptr, dtype=np.uint8)
    mat = [rVal, gVal, bVal]

    if slowPath:
        imgArray = imgArray.reshape((height, img.bytesPerLine()))
        editedArray = np.zeros((height, width, 3), dtype=np.int32)

        for index, line in enumerate(imgArray):
            line = line[:width * 3].reshape(width, 3)
            editedArray[index] = line + mat
            editedArray[index, editedArray[index] < 0] = 0
            editedArray[index, editedArray[index] > 255] = 255
    else:
        editedArray = np.array(imgArray.reshape((height, width, 3)), dtype=np.int32)
        # add values to each channel
        editedArray += mat
        editedArray[editedArray < 0] = 0
        editedArray[editedArray > 255] = 255

    editedArray = np.array(editedArray, dtype=np.uint8)

    return QImage(editedArray.data, editedArray.shape[1], editedArray.shape[0], width * 3, QImage.Format_RGB888)
