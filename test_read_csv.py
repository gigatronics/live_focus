# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:44:26 2018

@author: demoPC
"""



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
 