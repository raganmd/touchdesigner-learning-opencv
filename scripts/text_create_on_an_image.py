# creating a circle with openCV

# import libraries
import cv2
import numpy

# grab external image
imgFile 				= app.samplesFolder+'/Map/Banana.tif'
img						= cv2.imread(imgFile, 3)

# get the dimensions of the file
imgHeight, imgWidth 	= img.shape[:2]
print(imgWidth, imgHeight)

# variables for file locations
filePath 				= 'output/{file}.png'
fileName 				= "circle_banana_test"

# format the file path
filePath 				= filePath.format(file=fileName)

# find the center coordinates for drwaing the circle
circleX 				= int(imgWidth/2)
circleY 				= int(imgHeight/2)

circleRadius 			= 200

circleColor 			= (0,0,255)

circleThickness			= 5

# draw a circle with openCV
# color format is (Blue, Green, Red)
circle 					= cv2.circle( img, 
									  (circleX, circleY), 
									  circleRadius, 
									  circleColor, 
									  circleThickness)

# save the resulting image
cv2.imwrite(filePath, circle)