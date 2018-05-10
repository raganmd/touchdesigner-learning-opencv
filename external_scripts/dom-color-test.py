import cv2
import numpy
import sklearn

print("well, that worked... finally")


# save out an image from touch to a temporary location
colorImgTemp 			= "../cache/{file}.jpg"
colorImgFilePath 		= colorImgTemp.format(file="color1")

# open image with openCV
img 					= cv2.imread(colorImgFilePath, 1)
# print(img)

# transform image from bgr to rgb
img 					= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

img                     = img.reshape((img.shape[0] * img.shape[1], 3))

print(img)