# -*- coding: utf-8 -*-
"""

Created on Thu Oct 11 16:29:39 2018

@author: demoPC
"""



'''
test call exe from python
'''

import subprocess

cmd_dir = r'C:\Users\demoPC\Desktop\SuoCalibration_v2.6.0a\oCametry\application\checkerDetect'
cmd = r'\FindCodedChecker.exe '
img_dir = r'C:\Users\demoPC\py\lab_cam'
img = r'.\test_img2.png '
out = r'.\cam.txt'

def extract_pts(cmd_dir,cmd, img, out): #need dsc file in the current working dir
    full_cmd = cmd_dir+cmd+img+out
    print(full_cmd)
    subprocess.Popen(full_cmd)
    return out

#subprocess.Popen(r'dir')
#os.system(r"C:/Documents and Settings/flow_model/flow.exe") # r for raw string
#os.startfile(r"C:/Documents and Settings/flow_model/flow.exe")
#subprocess.call([r"C:/Documents and Settings/flow_model/flow.exe"])


'''
test reading in csv data
'''
import csv
import numpy as np
 
corners = []


#filename= r'./results/cam0.txt'

def read_csv(filename):
    with open(filename) as f:
        reader = csv.reader(f)
 #       print(next(reader))
        for row in reader:
            pt = np.array([row[3],row[4]])
            pt_int = [int(float(x))for x in pt]         # conv str to int
        #    print(pt_int)
            corners.append(pt_int)
    return corners

#print(pts[1][0])
 


'''
using jn's method
'''
import matplotlib.pyplot as plt
import cv2
import live_focus

def find_box(corners):
    x =[]
    y =[]
    for pt in corners:
        x.append(pt[0])
        y.append(pt[1])
    return (min(x),min(y)), (max(x), max(y))
#  return (min(pts), max(pts))
    

#out = extract_pts(cmd_dir,cmd,img,out)
corners= read_csv(out)
#rint(pts[0])


#show the points on image
img_file = r'test_img2.png'
img = cv2.imread(img_file)

# plot corners to verify
cv2.imshow('preview', img)
for pt in corners:
    cv2.circle(img, (pt[0],  pt[1]), 5, (0,255,0),-1)
    

# draw bounding box
rect = find_box(corners)
print(rect)
cv2.rectangle(img, rect[0], rect[1], (0, 255), 10)


# mask box region
crop = live_focus.crop2(img, rect)

# poly fit curve

# find_box

# analyze edges
sharpness=live_focus.calculate_sharpness(crop)
print(sharpness)

cv2.imwrite('img_preview.png', img)
#cv2.waitKey(0)

