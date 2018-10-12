
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





