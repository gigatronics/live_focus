# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 14:26:49 2018

@author: demoPC
"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import statprof

import timeit


def find_corners_cv(img):
#    img = cv2.imread('test_img2.png')
#    pattern_size = (6,9)
    ret, corners = cv2.findChessboardCorners(img, pattern_size)
    return corners

if __name__ == "__main__":    
    img = cv2.imread('test_img2.png')
    print(timeit.timeit("find_corners_cv()", setup="from __main__ import find_corners_cv"))


#statprof.start()
#
#try:
#
#
#
#ret, corners = cv2.findChessboardCorners(img, pattern_size)
#print(corners[0][0])
##print(int(corners[0][0]), int(corners[0][1]))
#
#
## plot corners to verify
#for corner in corners:
#    cv2.circle(img, (corner[0][0],  corner[0][1]), 5, (0,255,0), -1)
#
#cv2.imwrite('img2_preview.png', img)
#
#plt.imshow(img)
#plt.show()



#
#finally:
#    statprof.stop()
#    statprof.display()



'''
todo
    - profile / time the function call
    - install 
    
'''