
2018-10-10

objective: live sharpness measure

grab frames and display live on screen. PROBLEM: can compiling in terminal, but not in spyder. FIX: run spyder from terminal... now IDE is setup! 

where to find what functions to call? see ids manual here:
https://en.ids-imaging.com/manuals/uEye_SDK/EN/uEye_Manual_4.91/index.html

also here, for other ueye functions
C:\Users\demoPC\py\ids-pyueye-master\pyueye\ueye.py

-----------------

2018-10-11 

got the code up running.. used max to track peak sharpness, but noticed that it drifts over time (e.g. went from 0.9 up to 1.7)

improved the data that's displayed on screen




Todo: 
- suspect all sharpness values fits a gaussian, so max only shows the extreme cases. to verify, record all sharpness values, and see if they fits a gaussian curve. 
- possible to come up a formula based on stats, to determine a range for what sharpness value is acceptable.
- test in dark? 
- raise exceptions
- try JN's pattern
*- automatic tracking using JN's code? 



also, try JN's pattern:
> cd C:\Users\demoPC\Desktop\SuoCalibration_v2.6.0a\oCametry\application\checkerDetect
> FindCodedChecker.exe ./boardTag25h7_1.bmp cam  #cam is arbiturary name in case there are three camera present. 

interpretation of the results:
	tag: -1, c: 5, r: 8, x: 0.000000, y: 0.000000, z: 0.000000
	FOUND tag: 25, fam: t25h7, detection: 9, rotation: 3, position r: 7, c:3 from board: 0 (0 of target 0), at location r:1, c:2
	Consistent observation of board 0 (0), size 9 x 6, orientation: 270
	indexed corners: 54
	writing 9
	
	
1st col: the Id of the pattern it found (there is only 1 pattern in this file, so it's always 0)
2nd col: the Id of the corner (maps to the HEADER.dsc file, which describes the pattern and the position of each corner)
3rd col: 0 if the corner was not seen in the frame (useful for partial occlusion)
4th col: zero-based row id of the corner (in pixels)
5th col: zero-based column id of the corner (in pixels)


------



2018-10-12 friday

- git updated 
- triedto use JN's pattern.. call it directly from python.. turned out that needs 
- did a screen video capture showing the real time tuning.. "win G" to evoke the screen recording tool.. output file can be found here: C:\Users\demoPC\Videos\Captures

(cont'd) 2nd hypothesis that max_sharpness drifts because sensor noise.. so we need to manually set ini (config files) on the camera... to better understand the python wrapper on ueye sdk, i'm pip graphviz & pythoncallgraph to visualize the functions in the ueye.py file.

LIST OF GRAPHING TOOLS:
- pythoncallgraph
- gprof2dot

-------
  

2018-10-16 tuesday

load a camera parameter: 
- a quick way is to load a desired parameter, switch to trigger mode, and save to camera.. once saved, it will automatically when connecting the camera again next time. much easier to connect this way. 

JN's process:
- the corner finding algorithm is slow overall, because image  needs to be stored as a file, call exe, read in the image file and process... this is without calculating lines. can be very accurate, but certainly not real-time.

 

-----

2018-10-17 wed

JN's process (cont'ed)
- did poly fit and define a small region around corners and calc sharpness there.. compared it with my crude estimation

live tracking:
- tried checker corner finding algo from opencv, and turned out it's even slower~
- tried to use STATPROF, but didn't make it work, so defaulted to timeit.Timer
- go back to JN's exe, and try to clean up the rect and corners plots

next:
- find pattern? live tracking

----


2018-10-18 thur

live tracking:
- completed!!!


quick test using live tracking:
1. to do the inital focus, use live_focus.py
established procedure should be present the pattern
then use live_focus.py, select a region of interest (top left to bottom right)
2. to check if the lens perfipheral, where ROI auto recognizes the pattern, use live_track
3. pass on the  max from 1) to 2) for peripheral calculation



calibration
- the goal is to see if we can eliminate manually holding a pattern
- assumption: the calibration doesn't change if the camera rotates.. 
- idea: rotate the camera, rather than rotating the pattern
- captured two measurements:
1) sam holding the pattern walk around the camera
2) set the pattern up, and manually rotate the camera.. 
- next is to see good the calibraton is.. how different the model is. 


----

2018-10-19 friday

normalize
- wrote a function called calc_sharp_max() to calculate theoretical max 
(norm is in the range of 10e16, norm_per_pix is in the range of 10e8)
- when incorperated into live_focus try to normalize PP, the ratio is way too low (e-6)
- opt for meas / meas_max, 


NEXT: 
- refactoring..
- unit test.. e.g. assert


