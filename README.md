# ImageToString
An simple algorithm given any image generates a sequence of points that a string woven around the points gives a close approximation of the original image in real life.

# Usage
The code runs through commandline using argparse, and requires the images to remain in the same directory as the file.

Run ./ImageToString.py --help to see all arguments.

So far functionality includes:

Greyscale only (For now)
Circular image
 - Default size is Image size
 - Optional Radius (in pixels)
 - Optional circle center offset (x,y)
 - Variable number of points, Default = 200.
Square Images
 - Default size is image size
 - Optional arguments for square from two points (p1 & p2).
 - Points can also be changed in code (Need to work on this).
Iteration / Loop count.
  - Default = 4000

For best results, fiddle around with iteration and point values. 
More points = Better resolution
More loops = Better color/shade representation.
The drawback is longer computing times, and unreasonable real life needs.

# Example
![Milton 500-> 3500 lines](Examples/milton.png?raw=true)

<img src="Examples/line_4000jesus1.png?raw=true" width="350"><img src="Examples/line5000tommyc.png?raw=true" width="350">

# Planned

Color images
Test and fix square
Test and fix arguments (I threw it together quickly, it seems unrelaible at the moment).
Statistics (String required etc)
Beautify code further


# Credit

The code was written after watching [GoldPlatedGoofs video](https://youtu.be/-S_l8GGxOhU) on the topic, and I severely needed something to do through the holiday season. Highly recommended material as it kept me (somewhat) focused on the task.

Feedback is greatly appreciated! This is my first attempt at GitHub and non-hardware oriented programming in over a year, and I'd love to find a more elegant solution.
