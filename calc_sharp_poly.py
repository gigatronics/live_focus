# -*- coding: utf-8 -*-
"""

Created on Thu Oct 11 16:29:39 2018

@author: demoPC
"""



# test call exe from python
import subprocess
import csv
import numpy as np
import matplotlib.pyplot as plt
import cv2
import live_focus


# need dsc file in the current working dir
def extract_pts(cmd_dir,cmd, img, out): 
    full_cmd = cmd_dir+cmd+img+out
    print(full_cmd)
    subprocess.Popen(full_cmd)
    return out

# alternative methods
#subprocess.Popen(r'dir')
#os.system(r"C:/Documents and Settings/flow_model/flow.exe") # r for raw string
#os.startfile(r"C:/Documents and Settings/flow_model/flow.exe")
#subprocess.call([r"C:/Documents and Settings/flow_model/flow.exe"])


#    test reading in csv data
def read_csv(filename):
#    print(filename)
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
 

# test JN's method
def find_box(corners):
    x =[]
    y =[]
    for pt in corners:
        x.append(pt[0])
        y.append(pt[1])
    xpad = int((max(x)-min(x))*0.05)
    ypad = int((max(y)-min(y))*0.05)   
    return (((min(x)-xpad),(min(y)-ypad)), ((max(x)+xpad), (max(y)+ypad)))
#  return (min(pts), max(pts))


def fit_poly(corners):  # pts needs to be roughly on the same line
    x = []
    y = [] 
    z = []
    x = [corner[0] for corner in corners]
    y = [corner[1] for corner in corners] 
    z = np.polyfit(x, y, 2) # if degree=2, 3 coefficients z = p0 * x^n + p1 * x^(n-1) + p2
    rng = (corners[0][0],corners[-1][0]) # minX, minY
#    print(corners)
#    print(z)
#    print(rng)
    plt.plot(x,y,'o')
    return z, rng
   
    

def sample_pts(z, rng):
    '''
    return sample pts coordinates
    '''
    xp = np.linspace(rng[0],rng[1],10)
    yp = [np.polyval(z,x) for x in xp]
    plt.plot(xp,yp,'-')
#    print(int(xp), int(yp))
    return(xp,yp) 



def calc_sharpness_roi(corners,img):
    sharps=[]

    #calc area
    x = [int(corner[0]) for corner in corners]
    y = [int(corner[1]) for corner in corners]

    dist= np.sqrt(np.square(x[0]-x[1])+np.square(y[0]-y[1]))
    d = int(dist/3)            #arbiturary set. 0.33 of corner distance
   # print(dist)
    
    #extract pixel value
    for (xp, yp) in list(zip(x, y)):
#    for i in range(x):
#        print(xp,yp)
        img_nbyn=img[(yp-d):(yp+d), (xp-d):(xp+d)]
        sharpness=live_focus.calculate_sharpness(img_nbyn)
        sharps.append(sharpness)
    plt.imshow(img_nbyn)
    plt.show()
#    print(sharps) 
    sharp_jn = np.mean(sharps)
    sharp_jn_pp = sharp_jn/(4*d*d)
    return sharp_jn,sharp_jn_pp


    
def calc_sharp_max():
#   if os.path.exists(file):     
    img = cv2.imread('boardtag25h7_1.bmp')
    h,w = img.shape[0:2]
    size = h*w   
    sharp = live_focus.calculate_sharpness(img)
    sharp_per_pix = sharp/size   
    return sharp, sharp_per_pix

#def auto_track()


if __name__ == '__main__':
    
    SHARP_MAX = 9.06e+14            # the max iscalculated using calc_sharp_max.py
    SHARP_MAX_PER_PIX = 6.61e+08
    
    # set working directories
    cmd_dir = r'C:\Users\demoPC\Desktop\SuoCalibration_v2.6.0a\oCametry\application\checkerDetect'
    cmd = r'\FindCodedChecker.exe '
    img_dir = r'C:\Users\demoPC\py\lab_cam'
    img_file = r'.\test_img2.png '
    out = r'.\results\cam0.txt'

    corners = []    
    filename= r'.\results\cam0.txt'

    sharps_jn = []

    #out = extract_pts(cmd_dir,cmd,img,out)
    corners= read_csv(out)
    #rint(pts[0])
    
    
    # read in image file
    img_file = r'test_img2.png'
    img = cv2.imread(img_file)
    
    
    # poly fit curve
    z, rng = fit_poly(corners[0:6]) #  only pass corners on a line for fitting purposes  
   
    # calc sharpness from corners
    xp, yp = sample_pts(z, rng) # (2d+1)^2 area
    sharp_jn, sharp_jn_pp = calc_sharpness_roi(corners,img)      
    
    

    # plot corners to verify
    for corner in corners:
        cv2.circle(img, (corner[0],  corner[1]), 5, (0,255,0),-1)
    
    # draw bounding box
    rect = find_box(corners)
    print(rect)
    cv2.rectangle(img, rect[0], rect[1], (0, 255), 10)
     
    # mask box region
    crp = live_focus.crop2(img, rect)
    plt.subplot(121), plt.imshow(crp)
    plt.subplot(122), plt.plot([s for s in sharps_jn])
    plt.show()   
    
    # analyze edges
    sharp_gz = live_focus.calculate_sharpness(crp)
    sharp_gz_pp = sharp_gz/(crp.shape[0]*crp.shape[1])
   
    sharp_max, sharp_max_per = calc_sharp_max()
    
    print('gina method - sharp, sharp_pp: %.2g, %.2g' % (sharp_gz/SHARP_MAX, sharp_gz_pp/SHARP_MAX_PER_PIX))
    print('jn method - sharp, sharp_pp: %.2g, %.2g' % (sharp_jn/SHARP_MAX, sharp_jn_pp/SHARP_MAX_PER_PIX ))
      
    cv2.imwrite('img_preview.png', img)
    #cv2.waitKey(0)

