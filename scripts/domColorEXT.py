import sys
import cv2
import webbrowser
import numpy
from sklearn.cluster import KMeans

'''

'''

class DomColor:
	'''
		A tool for finding Dominant Color with openCV.

		python dependencies
		> numpy
		> scipy
		> sklearn
		> cv2
		> webbrowser
		> sys

		references
		> https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036
		> https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e
		> https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

		Notes
		---------------
		Your notes about the class go here
	'''

	def __init__(self):
		
		self.Clusters				= parent().par.Clusters
		self.PythonExternals		= parent().par.Pythonexternals
		self.TempFolder				= parent().par.Tempimagecache
		self.RampDAT				= op('ramp1_keys')
		self.SourceImgTOP			= op('null1')
		self.RampHeaders 			= ['pos', 'r', 'g', 'b', 'luminosity', 'a']
		self.ExternalsImport 		= False
		self.LuminList 				= []
		self.ColorsForDAT 			= []
		self.LuminRange 			= (0.2, 0.95)
		print("Dominant Color Init")

		return

	def Fill_ramp(self, sorted_colors=None):
		'''
			This is a sample method.

			The longer description goes here
			
			Notes
			---------------
			

			Args
			---------------


			Returns
			---------------
			
		'''	
		self.RampDAT.clear()
		self.RampDAT.appendRow(self.RampHeaders)

		# dummy check
		if sorted_colors == None:
			print("Fill_ramp() failed, missing args" )

		else:		
			# colors clean-up and prep
			for item in enumerate( sorted_colors ):
				# normalize vals
				colors_normalized   = [color_val / 255 for color_val in item[1]]

				# discard vals that are too bright or too dark
				if colors_normalized[-1] < self.LuminRange[0] or colors_normalized[-1] > self.LuminRange[1]:
					pass

				else:
					self.ColorsForDAT.append(colors_normalized)

			# send vals to DAT
			for item in enumerate(self.ColorsForDAT):
				pos                 = item[0] / ( len(self.ColorsForDAT) - 1)

				# add position
				item[1].insert(0, pos)

				# add in alpha val for ramp top
				item[1].append(1)

				self.RampDAT.appendRow(item[1])

		return

	def Process_image(self):
		'''
			This is a sample method.

			The longer description goes here
			
			Notes
			---------------
			

			Args
			---------------


			Returns
			---------------
			
		'''

		colorImgFilePath 		= "{project}/{temp}/temp_img.jpg".format(project=project.folder, temp=self.TempFolder)
		self.SourceImgTOP.save( colorImgFilePath , async=False )

		# open image with openCV
		img 					= cv2.imread(colorImgFilePath, 1)
		# transform image from bgr to rgb
		img 					= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# reshape the data
		img                     = img.reshape(img.shape[0] * img.shape[1], 3)

		kmeans                  = KMeans(n_clusters=self.Clusters.val)

		kmeans.fit(img)
		colors                  = kmeans.cluster_centers_
		labels                  = kmeans.labels_
		ramp_colors             = colors.astype(int)
		lumin_list              = []
		colors_forDAT            = []

		for color in enumerate(ramp_colors):
			R       = color[1][0]
			G       = color[1][1]
			B       = color[1][2]
			
			luminosity          = math.sqrt((0.299 * (R*R)) + (0.587 * (G*G)) + (0.114 * (B*B)))
			lumin_list.append(luminosity)

		color_and_lumin         = numpy.insert(ramp_colors, 3, lumin_list, axis=1)
		sorted_colors           = sorted(color_and_lumin, key=lambda x: x[3])

		self.Fill_ramp(sorted_colors)

		return


	def Import_external(self):
		'''
			This is a sample method.

			The longer description goes here
			
			Notes
			---------------
			

			Args
			---------------


			Returns
			---------------
			
		'''

		importHelp 				= 'http://derivative.ca/wiki099/index.php?title=Introduction_to_Python_Tutorial#Importing_Modules'
		messagBoxTitle			= 'Import Failure'
		messageBoxMessage		= '''\r
It looks like something when wrong importing
skLearn. Make sure you've added a path to your 
Python Externals library, and that you've sucessfully
installed sci-kit learn (sklearn) for your version
of Python.
'''
		messageBoxButtons		= ['Get Help', 'Close']
		pythonPath 				= "{}/".format(self.PythonExternals)

		# check to make sure the externals are in sys.path
		if pythonPath not in sys.path:
			sys.path.append(pythonPath)
		else:
			pass

		# check to see if we've imported sklearn yet
		if self.ExternalsImport:
			pass

		else:
			# safe attempts to check for sklearn module
			try:
				from sklearn.cluster import KMeans
				self.ExternalsImport 	= False
				print("Loading sklearn sucessful")

			# warn the user that import failed
			except:
				messageResults = ui.messageBox(	messagBoxTitle, 
												messageBoxMessage, 
												buttons=messageBoxButtons)

				if messageResults:
					pass

				else:
					# launch derivative wiki for help
					webbrowser.open(importHelp)

		return

	def Calculate_luminance(self, rgbVal=[0,0,0]):
		'''
			This is a sample method.

			The longer description goes here
			
			Notes
			---------------
			reference
			https://stackoverflow.com/questions/596216/formula-to-determine-brightness-of-rgb-color
			

			Args
			---------------
			rgbVal (list):
			> seomthing about that list here

			Returns
			---------------
			luminance (float):
			> something here about it
		'''

		R = rgbVal[0]
		G =	rgbVal[1]
		B = rgbVal[2]

		luminance = math.sqrt(0.299 * (R*R) + 0.587 * (G*G) + 0.114 * (B*B))

		return luminance