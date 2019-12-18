from PyQt5.QtGui import QImage
import numpy as np


def rgb2grayscale(img: QImage):
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    bytesPerPixel = img.byteCount()//(img.width()*img.height())
    # print('original image bpp:{}'.format(bytesPerPixel))

    if bytesPerPixel == 1:
        return img

    arr = np.asarray(ptr, dtype=np.uint8).reshape((img.height(), img.width(), bytesPerPixel))
    mat = [0.2989, 0.5870, 0.1140, 0] if bytesPerPixel == 4 else [0.2989, 0.5870, 0.1140]
    grayArr = np.array(np.dot(arr, mat), dtype=np.uint8)

    return QImage(grayArr, grayArr.shape[1], grayArr.shape[0], QImage.Format_Grayscale8)


def binarize(img: QImage, thr1, thr2):
    img = rgb2grayscale(img)  # convert it to grayscale first, we don't need RGB

    ptr = img.bits()
    ptr.setsize(img.byteCount())
    bytesPerPixel = img.byteCount() // (img.width() * img.height())
    arr = np.asarray(ptr).reshape((img.height(), img.width(), bytesPerPixel))
    condlist = [(arr < thr1), np.logical_and(arr > thr1, arr < thr2), (arr > thr2)]
    choicelist = [0, 85, 255]
    bin_arr1 = np.array(np.select(condlist, choicelist), dtype=np.uint8)

    return QImage(bin_arr1, bin_arr1.shape[1], bin_arr1.shape[0], QImage.Format_Grayscale8)

def rgbEdit(img: QImage, rVal, gVal, bVal):
    # TODO : Logic is broken, contorl works tho
    ptr = img.bits()
    ptr.setsize(img.byteCount())
    bytesPerPixel = img.byteCount()//(img.width()*img.height())

    arr = np.asarray(ptr).reshape((img.height(), img.width(), bytesPerPixel))
    # add values to each channel
    arr[:, :, 0] += rVal
    arr[:, :, 0] += gVal
    arr[:, :, 0] += bVal
    arr[arr < 0] = 0
    arr[arr > 255] = 255

    return QImage(arr, arr.shape[1], arr.shape[0], QImage.Format_ARGB32)