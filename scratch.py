# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 10:19:41 2019

@author: russ
"""

text   = "1 minute"

splits  = text.split( )
time_num   = float( splits[0] )
time_units = splits[1]
print( f"splits {splits}" )

print( f"time_num {time_num} time_units {time_units}" )



