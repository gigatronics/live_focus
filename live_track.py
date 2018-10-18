# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 14:42:07 2018

@author: demoPC
"""

from pyueye import ueye
import cv2
import numpy as np
#from scipy import stats

import matplotlib.pyplot as plt
import csv
import subprocess
import time
import os



def gray(image):
    return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def crop(image,r):
    x,y,delx,dely=r
    return image[y:y+dely,x:x+delx]

def crop2(image,pts):
#    x=pts[0][0]
#    y=pts[0][1]
#    dely=pts[1][1]-pts[0][1]
#    delx=pts[1][0]-pts[0][0]
    return image[pts[0][1]:pts[1][1],pts[0][0]:pts[1][0]]


def laplacian(image):
    return cv2.Laplacian(image,cv2.CV_64F,5)

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

def close_all(hcam): 
    ueye.is_StopLiveVideo(hcam, ueye.IS_FORCE_VIDEO_STOP)
    ueye.is_ExitCamera(hcam)
    print('stop video.. exit camera.. close all windows')    
    
def select_roi(image):
    fromCenter=False
    h,w,channel = image.shape
    image_copy = image
    if h>720:
        image_copy=cv2.resize(image,(0,0),fx=0.25,fy=0.25)
    r=cv2.selectROI("select roi please... press ENTER when done", image_copy, fromCenter) #x,y,delx,dely
    return (int(r[i]*4) for i in range(4))

def draw_rect(event,x,y,flags,param):
    global pts
    if event==cv2.EVENT_LBUTTONDOWN:
        print('start mouse position: %g %g' % (x,y))
        pts[0]=(x,y)
  #      pts[1]=(x,y) # to make sure both points are registered before calculating sharpness
        
    elif event==cv2.EVENT_LBUTTONUP:
        print('end mouse position: %g %g' % (x,y))
        pts[1]=(x,y)
    
#def stat(array):
#    median = np.median(array)
#    #mode = stats.mode(array, axis=None)
#    return median

#def auto_find_roi(image):
   

def init_cam(hcam):

    # get fps
  #  hcam_fps = is_GetFramesPerSecond(hcam, None)
    
    # set color mode
    ueye.is_SetColorMode(hcam, ueye.IS_CM_BGR8_PACKED) 
    
    # set region of interest
    rect_aoi = ueye.IS_RECT()
    rect_aoi.s32X = ueye.int(0)
    rect_aoi.s32Y = ueye.int(0)
    rect_aoi.s32Width = ueye.int(width)
    rect_aoi.s32Height = ueye.int(height)
    ueye.is_AOI(hcam, ueye.IS_AOI_IMAGE_SET_AOI, rect_aoi, ueye.sizeof(rect_aoi))

    # allocate memory
    mem_ptr = ueye.c_mem_p()
    mem_id = ueye.int()
    
    ueye.is_AllocImageMem(hcam, width, height, bitspixel, mem_ptr, mem_id)
    ueye.is_SetImageMem(hcam, mem_ptr, mem_id)
     
    # continuous capture to memory
    ueye.is_CaptureVideo(hcam, ueye.IS_DONT_WAIT)
    
    return mem_ptr
      

def extract_corners(cmd_dir,cmd, img, out): #need dsc file in the current working dir
    full_cmd = cmd_dir+cmd+img+out
    print('extracting... %s' % full_cmd)
    subprocess.Popen(full_cmd)
    return out


def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
 #       print(next(reader))
        for row in reader:
            pt = np.array([row[3],row[4]])
            pt_int = [int(float(x))for x in pt]         # conv str to int
        #    print(pt_int)
            if pt_int != [0, 0]:                        # discard (0,0)
                pts.append(pt_int)
#    print(pts[0])
    return pts


def check_agst_zero(v): # make sure always positive
    return max(0, v)


def find_box(corners):
#    try:
    
    x =[]
    y =[]
    for pt in corners:
        x.append(pt[0])
        y.append(pt[1])
    xpad = int((max(x)-min(x))*0.05)
    ypad = int((max(y)-min(y))*0.05) 
    # checks to make sure box is within image.. 
    x1 = max(1, min(x)-xpad)
    y1 = max(1, min(y)-ypad)
    x2 = min(width, max(x)+xpad)
    y2 = min(height, max(y)+ypad)
    return((x1, y1),(x2, y2))
#
#    except ValueError: 
#        print('no corners extracted. check cam.txt file.' )
        
    #return (((min(x)-xpad),(min(y)-ypad)), ((max(x)+xpad), (max(y)+ypad)))


def find_corners_cv(img):
    pattern_size = (6,9)
    ret, corners = cv2.findChessboardCorners(img, pattern_size)
    return corners

    
if __name__=="__main__":
    global width
    global height
    global bitspixel
    global corners
       
    width = 3088
    height = 2076
    bitspixel = 24 # for colormode = IS_CM_BGR8_PACKED
       
    cmd_dir = r'C:\Users\demoPC\Desktop\SuoCalibration_v2.6.0a\oCametry\application\checkerDetect'
    cmd = r'\FindCodedChecker.exe '
    img_dir = r'C:\Users\demoPC\py\lab_cam'
    img_name = r'.\img_temp.png '
#    out = r'.\cam.txt'
    
    sharpness=0
    sharps=[] 
    sharp_max=0 
    sharp_smooth=0
    sharp_med=0
    
    x,y,delx,dely = int(width/4),int(height/4),int(width/8),int(height/8)
    pts = []
    corners = []
     
    # initialize camera
    hcam =ueye.HIDS(0)
    ret = ueye.is_InitCamera(hcam, None)
    print("camera intialized %g" % ret)
 
    mem_ptr = init_cam(hcam)
    
    # get data from camera and display
    lineinc = width * int((bitspixel + 7) / 8)
 
 #   f = open('data.txt', 'a+')
    
    i = 0
    
    try:         
        while True:
            # grab frame
            img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
            img = np.reshape(img, (height, width, 3))
            
            if (np.mod(i,10)==9):            
                # write frame to file       
                #print(img.shape)
                print('new frame acquired!')
                cv2.imwrite('img_temp.png', img)
                time.sleep(2)
              
                # call exe and file to extract corners and save to cam.txt
                out = extract_corners(cmd_dir,cmd,'img_temp.png',' cam')
                time.sleep(2)
                
                if os.path.exists("cam0.txt"):
                    corners = read_csv('cam0.txt')
                             
                # draw bounding box
                time.sleep(3)
                rect = find_box(corners) 
#                print(rect)               
                
                # mask box region
                crp = crop2(img, rect)
            
                # analyze edges
                sharpness=calculate_sharpness(crp)
            
                if sharpness > sharp_max:
                    sharp_max =sharpness    
                    print("sharpness changed, peaked at %.2e" % sharp_max)                    
     
                print('sharpness at %.2e' % sharpness)
                print('peak sharpness: %0.2e' % sharp_max)
                
                
                # plot corners to verify
                for pt in corners:
                    cv2.circle(img, (pt[0],  pt[1]), 5, (0,255,0), -1)
                        
                preview = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.rectangle(preview, tuple([int(x/2) for x in (rect[0])]), tuple([int(x/2) for x in (rect[1])]), (0, 255), 10)
                cv2.putText(preview, 'maximum = %.2e' % (sharp_max), (50,50), font, fontScale=1, color=(0,255,0), thickness=2)
                cv2.putText(preview, 'sharpness = %.2e' % (sharpness), (50, 100), font, fontScale=1, color=(0,255,0), thickness=2)     
     #              cv2.imshow('preview', preview)             
    
                plt.imshow(preview)
                plt.show()
    
    
                print('found %g corners: ' % len(corners))
      
    #           # clear txt file and reset text file
                if os.path.exists('cam0.txt'):
                    os.remove('cam0.txt')
                
                # remove circle drawing
                for pt in corners:
                    cv2.circle(img, (pt[0],  pt[1]), 5, (0,255,255), -1)
                #cv2.imshow('preview', img)
    
                # delete corners
                del corners[:]
     #               corners[:] = []
                           
            i+=1
        
    finally:
        close_all(hcam)
        cv2.destroyAllWindows()
        


'''
todo:
    - refresh the dots
    x- refresh cam0.txt
    x- fix camera auto stuck on.. 
    -
    - TROUBLESHOOT NEXT:
    - opencv is not responding
    - "corners" are flushed  ?!!!!!????
    - dots are not removed
    - 
'''