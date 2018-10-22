from pyueye import ueye
import cv2
import numpy as np
#from scipy import stats
#import matplotlib.pyplot as plt


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
    pts = sorted(pts)           # in case the rect is selected from bottom right to top left 
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
   
def calc_sharp_max(img):
#   if os.path.exists(file):     
    img = cv2.imread('boardtag25h7_1.bmp')
    h,w = img.shape[0:2]
    size = h*w   
    sharp = calculate_sharpness(img)
    sharp_per_pix = sharp/size   
    return ['%.2e %.2e' % (sharp, sharp_per_pix)]






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
#    
#    # set parameters, see ids doc for parameter setting flow chart
#    ueye.is_PixelClock(hcam, ueye.IS_PIXELCLOCK_CMD_GET, exp, ueye.sizeof(pclock))
#    pclock = ueye.int(220)
#    ueye.is_PixelClock(hcam, ueye.IS_PIXELCLOCK_CMD_GET, pclock, ueye.sizeof(pclock))
#    
#    expo_rng = ueye.is_Exposure(hcam, IS_EXPOSURE_CMD_GET_CAPS, ncap, size(ncap))
#    ftime_rng = ueye.is_GetFrameTimeRange()
#    expo_rng = (expo_rng[0], max(expo_rng[1], ftime_rng[1]))
#    
#    fps_actual = ueye.cdouble() 
#    ueye.is_SetFrameRate(hcam, ueye.cdouble(fps_set), byref(fps_actual))
#    
#    exp_cap = ueye.uint32()
#    ueye.is_Exposure(hcam, ueye.IS_EXPOSURE_GET_EXPOSURE_RANGE, ueye.byref(exp_cap), ueye.sizeof(exp_cap))
#    exp_cur = ueye.cdouble() # in s
#    ueye.is_Exposure(hcam, ueye.IS_EXPOSURE_SET_EXPOSURE, ueye.byref(exp_cur), ueye.sizeof(exp_cur))

#    ueye.is_SetGainBoost()
#    ueye.is_Gamma()
#    ueye.is_SetHWGainFactor()
#    
    
    # allocate memory
    mem_ptr = ueye.c_mem_p()
    mem_id = ueye.int()
    
    ueye.is_AllocImageMem(hcam, width, height, bitspixel, mem_ptr, mem_id)
    ueye.is_SetImageMem(hcam, mem_ptr, mem_id)
     
    # continuous capture to memory
    ueye.is_CaptureVideo(hcam, ueye.IS_DONT_WAIT)
    
    return mem_ptr
    
    
if __name__=="__main__":
    global width
    global height
    global bitspixel
    
    SHARP_MAX = 9.06e+14            # the max iscalculated using calc_sharp_max.py
    SHARP_MAX_PER_PIX = 6.61e+08
    
    sharpness=0
    sharps=[] 
    sharp_max=0.1 
    sharp_smooth=0
    sharp_med=0  
   
    width = 3088
    height = 2076
    bitspixel = 24 # for colormode = IS_CM_BGR8_PACKED
     
    x,y,delx,dely = int(width/4),int(height/4),int(width/8),int(height/8)
    pts=[(10,10),(0,0)]

    
    # initialize camera
    hcam =ueye.HIDS(0)
    ret = ueye.is_InitCamera(hcam, None)
    print("camera intialized %g" % ret)
 
    mem_ptr = init_cam(hcam)
    
    # get data from camera and display
    lineinc = width * int((bitspixel + 7) / 8)
 
    f = open('data.txt', 'a+')
    try:
        while True:
            img = ueye.get_data(mem_ptr, width, height, bitspixel, lineinc, copy=True)
            img = np.reshape(img, (height, width, 3))
            crp = crop2(img,pts)
            w,h = crp.shape[0:2]
            gry = gray(crp)      
          
            if not ((0,0) in pts):
                sharpness = calculate_sharpness(gry)
                sharps.append(sharpness)                # write to a var for dbg
                f.write(str(sharpness))                 # write to a file for dbg
                sharp_smooth = np.mean(sharps[-100:])
                sharp_med = np.median(sharps)  
    
                if sharpness > sharp_max:
                    sharp_max =sharpness    
                    print("sharpest: %.2e" % sharp_max)
                
            preview = cv2.resize(img, (0,0), fx=0.5, fy=0.5) 
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(preview, 'targe1(max) = %.2e, target2(med) = %.2e ' % (sharp_max, sharp_med), (50,50), font, fontScale=1, color=(0,255,0), thickness=2)
            cv2.putText(preview, 'sharp_meas = %.2e ' % (sharpness), (50, 100), font, fontScale=1, color=(0,255,0), thickness=2)
            cv2.putText(preview, 'sharp_norm1(phuc) = %.2g, sharp_norm2(rel) = %0.2g ' % (sharpness/SHARP_MAX, sharpness/sharp_max), (50, 150), font, fontScale=1, color=(0,255,0), thickness=2)
            cv2.putText(preview, 'sharp_norm1_PP(phuc) = %.2g ' % (sharpness/(w*h)/SHARP_MAX_PER_PIX), (50, 200), font, fontScale=1, color=(0,255,0), thickness=2)
            cv2.setMouseCallback('preview',draw_rect)
            
            if not ((0,0) in pts):
                cv2.rectangle(preview, pts[0],pts[1], color=(0,255,0),thickness=2)#, lineType=4)
    
            cv2.imshow('preview', preview)        
            
            if cv2.waitKey(1) & 0xFF == '27':
                break
            
    finally:
        close_all(hcam)
        cv2.destroyAllWindows()
        
'''
todo:
   > - add framerate on screen... 
   x - speed up by analyzing only the cropped region
   x - either auto find roi based on intensity or pattern matching, or select roi...
   - try sobel and see if it's this sensitive.. 
    - collect all sharpness values and change max.. 
    - try jn's pattern.. auto pattern matching
    - auto track pattern?
    
'''
    