# creating a circle with openCV

# import libraries
import cv2
import numpy

# set up numpy array
img			= numpy.zeros( (512,512,3), numpy.uint8 )

# variables for file locations
filePath 	= 'output/{file}.png'
fileName 	= "circle_test"

# format the file path
filePath 	= filePath.format(file=fileName)

# draw a circle with openCV
circle 		= cv2.circle(img, (447, 63), 63, (0,0,255), -1)

# save the resulting image
cv2.imwrite(filePath, circle)