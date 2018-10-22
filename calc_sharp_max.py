# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 16:07:53 2018

@author: demoPC




"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def edge(image):
    sy = cv2.Sobel(image,ddepth=cv2.CV_64F,dx=0,dy=1,ksize=5)
    sx = cv2.Sobel(image,ddepth=cv2.CV_64F,dx=1,dy=0,ksize=5)
    return (np.power(np.hypot(sx,sy),2))
    
def calculate_sharpness(image):
#    lap = laplacian(image)
#    sharpness=lap.flatten().var()
    edg = edge(image)
    sharpness=edg.flatten().var()
    return sharpness

#def calc_sharp_max(img):
##   if os.path.exists(file):     
##    img = cv2.imread('boardtag25h7_1.bmp')
#    h,w = img.shape[0:2]
#    size = h*w   
#    sharp = calculate_sharpness(img)
#    sharp_per_pix = sharp/size   
#    return ['%.2e %.2e' % (sharp, sharp_per_pix)]


if __name__ == '__main__':
    
    # read in an image
    img = cv2.imread('boardtag25h7_1.bmp') 
    
    
    # apply a few gaussian blur
    img_blur = cv2.GaussianBlur(img, (15,15), 0)
    img_blur1 = cv2.medianBlur(img, 49)
    img_blur2 = cv2.medianBlur(img, 99)


    # calculate
#    sharp, sharp_per_pix = calc_sharp_max(img)

#    print('max sharpness is %.2e ' % sharp)
#    print('sharp per pix is %.2e ' % sharp_per_pix)
#      
    print(calc_sharp_max(img))
    print(calc_sharp_max(img_blur))
    print(calc_sharp_max(img_blur1))
    print(calc_sharp_max(img_blur2))

    
    # plot
    plt.subplot(221), plt.imshow(img), plt.title('original - ' +str(calc_sharp_max(img)))
#    plt.text(10, 10, calc_sharp_max(img), fontsize=12)
    plt.subplot(222), plt.imshow(img_blur), plt.title('guassian blur - '+str(calc_sharp_max(img_blur)))
 #   plt.text(10, 10, calc_sharp_max(img_blur), fontsize=12)
    plt.subplot(223), plt.imshow(img_blur1), plt.title('median blur 49 - '+str(calc_sharp_max(img_blur1)))
  #  plt.text(10, 10, calc_sharp_max(img_blur1), fontsize=12)
    plt.subplot(224), plt.imshow(img_blur2), plt.title('median blur 99 - '+str(calc_sharp_max(img_blur2)))
   # plt.text(10, 10, calc_sharp_max(img_blur2), fontsize=12)

    