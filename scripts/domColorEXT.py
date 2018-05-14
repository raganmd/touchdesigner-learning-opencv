'''
	matthew ragan | matthewragan.com
'''

import sys
import os
import cv2
import webbrowser
import numpy
from sklearn.cluster import KMeans

class DomColor:
	'''
		A tool for finding Dominant Color with openCV.

		Here we find an attempt at locating dominant colors from a source image with openCV
		and KMeans clustering. The large idea is to sample colors from a source image build
		averages from clustered samples and return a best estimation of dominant color. While
		this works well, it's not perfect, and in this class you'll find a number of helper
		methods to resolve some of the shortcomings of this process. 

		Procedurally, you'll find that that the process starts by saving out a small
		resolution version of the sampled file. This is then hadned over to openCV
		for some preliminary analysis before being again handed over to sklearn
		(sci-kit learn) for the KMeans portion of the process. While there is a built-in
		function for KMeans sorting in openCV the sklearn method is a little less cumbersom
		and has better reference documentation for building functionality. After the clustering
		process each resulting sample is processed to find its luminance. Luminance values
		outside of the set bounds are discarded before assembling a final array of pixel values
		to be used. 

		It's worth noting that this method relies on a number of additional python libraries.
		These can all be pip installed, and the recomended build appraoch here would be to
		use Python35. In the developers experience this produces the least number of errors
		and issues - and boy did the developer stumble along the way here.

		python dependencies
		> numpy
		> scipy
		> sklearn
		> cv2

		references
		> https://buzzrobot.com/dominant-colors-in-an-image-using-k-means-clustering-3c7af4622036
		> https://gist.github.com/skt7/71044f42f9323daec3aa035cd050884e
		> https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

		ToDo
		---------------
		[ ] consider a slightly different approach vs. using a ramp TOP
		[ ] look into running the openCV process in another thread to avoid blocking
		[ ] add button to allow the user to check if all the python bits have been imported
	'''

	def __init__(self):
		
		self.Clusters				= parent().par.Clusters
		self.PythonExternals		= parent().par.Pythonexternals
		self.TempFolder				= parent().par.Tempimagecache
		self.RampDAT				= op('ramp1_keys')
		self.SourceImgTOP			= op('null1')
		self.RampHeaders 			= ['pos', 'r', 'g', 'b', 'luminosity', 'a']
		self.LuminList 				= []
		self.ColorsForDAT 			= []
		self.LuminRange 			= (0, 1)

		self.GlslTOP 				= op('glslmulti1')
		print("Dominant Color Init")

		return

	def Fill_ramp(self, sorted_colors=None):
		'''
			Fill the target network ramp with dominant colors.

			While this is not a partciularly exciting process, this is an essentail element
			in the resulting process. This clears a table DAT of any results, then first
			normalizes the results, discards vals that are outside of the set luminosity range
			then fills in the target table with the results. This is the last step in the 
			process of finding dominant color
			
			Notes
			---------------
			

			Args
			---------------
			sorted_colors (numpy_array)
			> a list of lists containing the results of the KMeans process. These are
			> used to generate the final pixel values that are returned from this
			> module.

			Returns
			---------------
			none
		'''	
		# clear and setup ramp for new keys
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
			
			self.GlslTOP.par.resolutionw 	= len(self.ColorsForDAT)

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
		colorImgDir 			= "{project}/{temp}".format(project=project.folder, temp=self.TempFolder)

		# clear previous results
		self.LuminList 			= []
		self.ColorsForDAT 		= []

		# grab bounds parameters
		self.LuminRange 		= (parent().par.Lbounds1.val, parent().par.Lbounds2.val)

		# check to see if the temp directory exists and make it if it's not there
		self.Check_path(colorImgDir)

		self.SourceImgTOP.save( colorImgFilePath , async=False )

		# open image with openCV
		img 					= cv2.imread(colorImgFilePath, 1)
		# transform image from bgr to rgb
		img 					= cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

		# reshape the data
		img                     = img.reshape(img.shape[0] * img.shape[1], 3)

		# kmeans process
		kmeans                  = KMeans(n_clusters=self.Clusters.val)
		kmeans.fit(img)
		colors                  = kmeans.cluster_centers_
		labels                  = kmeans.labels_
		ramp_colors             = colors.astype(int)
		lumin_list              = []
		colors_forDAT           = []

		# calculate and add luminosity to the color
		for color in ramp_colors:
			lumin_list.append(self.Calculate_luminance(color))

		# add luimin to numpy array, sort based on luminosity
		color_and_lumin         = numpy.insert(ramp_colors, 3, lumin_list, axis=1)
		sorted_colors           = sorted(color_and_lumin, key=lambda x: x[3])

		# fill ramp colors
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

		luminance = math.sqrt((0.299 * (R*R)) + (0.587 * (G*G)) + (0.114 * (B*B)))

		return luminance
	
	def Check_path(self, colorImgDir):
		'''
			This is a sample method.

			The longer description goes here
			
			Notes
			---------------
			

			Args
			---------------
			colrImgDir (str):
			> a file path to check for existing

			Returns
			---------------
			none
		'''
		if os.path.isdir(colorImgDir):
			pass
		else:
			os.mkdir(colorImgDir)
		return