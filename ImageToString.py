#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from math import pi

import skimage
from skimage import io, img_as_float
from skimage.draw import line
from skimage.color import rgb2gray
import numpy as np

import argparse

class ImageToString:
	
	def __init__(self, input_file,iteration=4000,npoints = 200,radius=0,offsetx = 0, offsety = 0,square=False, sqp1=(0,0),sqp2=True):
		
		self.input_file = input_file
		self.square = square
		self.npoints = npoints
		self.sqp1 = sqp1
		self.sqp2 = sqp2
		self.offsetx = offsetx
		self.offsety = offsety
		self.radius = radius
		self.iteration = iteration
		self.linelength = []
		self.synthdata = []
		self.points = []
	
	# Find pixels for N points in a circle. More points = Better resolution.
	def points_on_circumference(self): 
		self.points =  [
	        (
	            int(self.center[0] + (math.cos(2 * pi / self.npoints * x) * self.radius)),  # x
	            int(self.center[1] + (math.sin(2 * pi / self.npoints * x) * self.radius))  # y
			) 
				for x in range(0, self.npoints + 1)]
	
	# Find pixels in a square defined by p1 -> p2. Defaults to image size.
	def points_on_square(self, inc=5): 
		self.points = []
		if self.sqp2 == True:
			self.sqp2 = (self.image.shape[0] - 1, self.image.shape[1] - 1) # im.shape - (1,1) returns lowest right corner pixel. Is there a easier way?
		width = self.sqp2[0] - self.sqp1[0]
		height = self.sqp2[1] - self.sqp1[1]
		for x in range(0,height,inc): # Manually change inc for x/y if you need more points along one axis.
			self.points.append((x+self.sqp1[0],self.sqp1[1]))
			self.points.append((x+self.sqp1[0],self.sqp2[1]))
		for y in range(0,width,inc):
			self.points.append((self.sqp1[0],y+self.sqp1[1]))
			self.points.append((self.sqp2[0],y+self.sqp1[1]))
	
	# Get pixels between two points.
	def GetLine(self,p1,p2):
		rr,cc = line(int(self.points[p1][0]),int(self.points[p1][1]),int(self.points[p2][0]),int(self.points[p2][1]))
		return rr,cc
	
	# We found the points we wish to edit; Now we edit the image.
	def FillLine(self,p1, p2, Bthick = 1.1, Wthick = 0.1):
		rr,cc = self.GetLine(p1,p2)
		self.linelength.append(len(rr)) # Save line length: Sum of list is total length of string needed.
		self.synthdata.append(p2) # Save points for speech synthesis. (Consider saving only p2?)
		self.image_out[rr,cc] = self.image_out[rr,cc] / Bthick # Draw black line on image 2: Every iteration gives 10% darker pixel values.
		self.image[rr,cc] = self.image[rr,cc] + Wthick # Draw white line on image 1: Every iteration gives 10% lighter pixel values(?).
		
		# Bthick, WThick
		# These values need to be adjusted according to the string.
		# Current values result in beautiful images digitally, although real life images are untested.
		# Theoretically this should work.
	
	# Iterate through all points and calculate pixel values. Lowest average is our next dark string.
	def NextLine(self,p1):
		val = []
		for x in range(0,len(self.points)):
			rr,cc = self.GetLine(p1,x)
			val.append(np.mean(self.image[rr,cc]))
		p2 = val.index(min(val))
		self.FillLine(p1,p2)
		return p2
	
	def Save(self):
		imageout = "line_" + str(self.iteration) + self.input_file
		io.imsave(imageout, self.image_out)
		print("Image saved as " + imageout + " in original image directory.")	
		np.savetxt("Line_" + self.input_file + "_data", self.synthdata, fmt='%i')
		print("Position data saved as " + imageout + "_data!")

	# Experimental: Trying to estimate how much string is needed for an image.
	# def Statistics(self): 
		# m = sum(self.totallength) * self.radius / self.rlradius
		# print("Image diameter of: " + str(diameter))
		# print("{0:.2f}".format(m) + " m of string")
		# print(str(len(linelen)) + "loops")
	
	def run(self):
		self.image = io.imread(self.input_file) # Open image
		print("ImageToSring on: " + self.input_file + "!")
		self.image = rgb2gray(self.image)
		nrows, ncols = self.image.shape
		self.image_out = np.full((nrows, ncols), 255, dtype=np.uint8)

		if self.square:
			self.points_on_square()
		else:
			if self.radius == 0:
				 self.radius = min(self.image.shape)/2 - 1
			self.center = (nrows/2) - self.offsety,(ncols/2) - self.offsetx
			self.points_on_circumference() 	
		n = 0
		for x in range(0,self.iteration):
			if x % 500 == 0:
				print(str(x) + " Iterations out of " + str(self.iteration))
			n = self.NextLine(n)
		#self.Statistics() # Not working atm.
		self.Save()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Generate continous string images!")
	
	parser.add_argument(
			'-i',
			'--input',
			dest='input_file',
			help='input file name'						
			)
	
	parser.add_argument(
			'-l',
			'--loops',
			default=4000,
			type=int,
			dest='nloop',
			help='Amount of loops/windings around points'
			)
	
	parser.add_argument(
			'-p',
			'--points',
			default=200,
			type=int,
			dest='npoints',
			help='Amount of points in circular image'
			)
	
	parser.add_argument(
			'-r',
			'--radius',
			default=0,
			type=int,
			dest='radius',
			help='optional radius of circular edge, defaults to image size.'
			)
	
	parser.add_argument(
			'-x',
			'--offsetx',
			default=0,
			type=int,
			dest='offsetx',
			help='Offset circle center in the 1st axis.' #Explain further +/-.
			)
	
	parser.add_argument(
			'-y',
			'--offsety',
			default=0,
			type=int,
			dest='offsety',
			help='Offset cricle center in the 2nd axis.' #Expalin further +/-
			)
	
	parser.add_argument(
			'-s',
			'--square',
			default=False,
			type=bool,
			dest='square',
			help='Boolean, Use square shape as image outline rather than default circle.'
			)
	
	parser.add_argument(
			'-p1',
			'--squarep1',
			default=(0,0),
			type=tuple,
			dest='sqp1',
			help='Tuple, Define upper-left corner of square edge. Defaults to (0,0).'
			)
	
	parser.add_argument(
			'-p2',
			'--squarep2',
			default=True,
			type=tuple,
			dest='sqp2',
			help='Tuple, Define lower-right corner of square edge. Defaults to image size.'
			)
	
	args = parser.parse_args()
	print(args)
	
	ImageToStringObj = ImageToString(
					args.input_file,
					args.nloop,
					args.npoints,
					args.radius,
					args.offsetx, 
					args.offsety,
					args.square, 
					args.sqp1,
					args.sqp2
					)
	ImageToStringObj.run()
