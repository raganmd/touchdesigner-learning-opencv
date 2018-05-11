'''
    finding dominant color with openCV

    dependencies
    > numpy
    > scipy
    > sklearn

    references
    > https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036
    > https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e
    > https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/
'''

# import libraries
import sys
import cv2

readyToProcess          = False

mypath = "C:\\Program Files\\Python35"
if mypath not in sys.path:
    sys.path.append(mypath)

try:
    from sklearn.cluster import KMeans
    readyToProcess      = True
    print("Ready to Process")

except:
    print("Missing Library")



colorImgTemp 			= "cache/{file}.jpg"
colorImgFilePath 		= colorImgTemp.format(file="color1")
imgFileTOP 				= op('null1')
clusters                = 10
rampTableDAT            = op('ramp1_keys')

if readyToProcess:
    # save out an image from touch to a temporary location
    imgFileTOP.save( colorImgFilePath , async=False )

    # open image with openCV
    img 					= cv2.imread(colorImgFilePath, 1)
    # transform image from bgr to rgb
    img 					= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # reshape the data
    img                     = img.reshape(img.shape[0] * img.shape[1], 3)

    kmeans                  = KMeans(n_clusters=clusters)

    kmeans.fit(img)
    colors                  = kmeans.cluster_centers_
    labels                  = kmeans.labels_
    ramp_colors             = colors.astype(int)


    new_ramp_colors = sorted(ramp_colors, key=lambda x: x[0])


    rampTableDAT.clear()
    header                  = ['pos', 'r', 'g', 'b', 'a']
    rampTableDAT.appendRow(header)

    for item in enumerate( new_ramp_colors ):
        # normalize vals
        colors_normalized   = [color_val / 255 for color_val in item[1]]

        # calculate position val
        pos                 = item[0] / (len(ramp_colors) - 1)

        colors_normalized.insert(0, pos)
        colors_normalized.append(1)

        rampTableDAT.appendRow(colors_normalized)

else:
    pass
