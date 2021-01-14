from __future__ import division
from lyse import *
from pylab import *
from analysislib.common import *
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from gaussian2d import *
import matplotlib.patches as patches
import cv2

def get_images():
    fluo = run.get_image(orientation='YZ', label = 'fluo_img', image='fluo_img')
    # orig_fluo = np.copy(fluo)

    return np.array(fluo)
    
df = data(path)
run = Run(path)
img = get_images()
print(img.dtype)
print(img)
img = img
# img = cv2.imread('opencv_logo.png',0)
# img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
img = img.astype(np.uint8)
print(img)
print(img.dtype)


circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,200)

circles = np.uint16(np.around(circles))
print(circles)
# for (x, y, r) in circles[0]:
		# # draw the circle in the output image, then draw a rectangle
		# # corresponding to the center of the circle
	# cv2.circle(img, (x, y), r, (0, 255, 0), 4)
    
    
# cv2.imshow('detected circles',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

