#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from math import pi
import numpy as np
from skimage import io
from skimage.viewer import ImageViewer
from skimage.color import rgb2gray
from skimage.draw import line
from skimage import img_as_ubyte

ImagePath = "Examples/Milton.jpeg"              # Path to image

# Open Image
ImageData = io.imread(ImagePath) # Open Image
ImageData = rgb2gray(ImageData)  # Convert to grayscale
# To support color the image needs to be broken into it's primary colors (See Color Quantization)
# Then the image can be built up of the colored strings equal to the quantizied colors.

# Configuration
Nails = 200;                                    # Amount of points for to wrap image around
Iteration = 3000;                               # How many loops between points until program stops.

NRows, NCols = ImageData.shape                  # Image width and Height
Center = [NRows/2, NCols/2]                     # Defaults to center
XWidth = min(NRows, NCols)/2 - 1                # Defaults to smallest width. Added X / Y width to support ovals.
YWidth = XWidth
                                                # Generate nail positions.
Points =  [
	            (
	            int(Center[0] + (math.cos(2 * pi / Nails * x) * XWidth)),  # x
	            int(Center[1] + (math.sin(2 * pi / Nails * x) * YWidth))  # y
		    )
                for x in range(0, Nails + 1)]

# To recreate the image on a real canvas, you'll need to decide a canvas size, and use the above function to generate proper nail functions.
# I suggest using a graphing program (GeoGebra) to create N points in a circle pattern and printing it to scale on paper. (Tried and tested, It works pretty well)
# If you have access to a Lasercutter or CNC machine, use that to mark holes on wood and add nails or bolts. (Haven't tried this yet, but far less of a hazzle)


# Generate Blank Image
StringData = np.full((NRows, NCols), 255, dtype=np.uint8)   # Pure white image that we draw black lines on. Gives you an idea what the real result is.

# Calculate string
p1 = 0
for x in range(0, Iteration):                   # Iterate through all loops.
    if x % 500 == 0:
        print(x)

    meanColorVal = []   # N-Mean Color Values.
                                                
    for p2 in range(0, Nails):                  # Find darkest line in this iteration.
        rr, cc = line(Points[p1][0], Points[p1][1], Points[p2][0], Points[p2][1])       # Get line from P1 and P2, Save all pixels to RR and CC.
        meanColorVal.append(np.mean(ImageData[rr,cc]))                                  # Save average color value of pixels in line to Mean Color Data.
                                                                                        # Repeat Nails amount of times

    p2 = meanColorVal.index(min(meanColorVal))  # Find darkest line (0 = Black). Index in meanColorVal = Index in Nails.

    rr, cc = line(Points[p1][0], Points[p1][1], Points[p2][0], Points[p2][1])           # Save darkest line into buffer again 
    ImageData[rr,cc] = ImageData[rr, cc] + 0.1                                          # Lighten original image (Float64 type)
    StringData[rr,cc] = StringData[rr, cc] / 1.1                                        # Darkest string image (Uint8 type)

    p1 = p2                                                                             # P2 becomes P1 in next iteration.

# Its important to note that best results are achieved by lightening and darkening the image slightly.
# In real life a string isn't 100% black, but several strings overlaid achieve a higher blackness.
# If you have thick strings, you might want to change the values above slightly.
# I found my values simply by guessing and it worked pretty well. I have yet to find a logic in it.

# Display String image
viewer = ImageViewer(ImageData)
viewer.show()
viewer = ImageViewer(StringData)
viewer.show()


