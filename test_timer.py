# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 15:17:54 2018

@author: demoPC
"""

def test():
    """Stupid test function"""
    L = []
    for i in range(100):
        L.append(i)

if __name__ == '__main__':
    import timeit
    print(timeit.timeit("test()", setup="from __main__ import test"))