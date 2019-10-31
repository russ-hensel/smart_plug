# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 10:19:41 2019

@author: russ
"""

def ex_parse():
    text   = "1 minute"

    splits  = text.split( )
    time_num   = float( splits[0] )
    time_units = splits[1]
    print( f"splits {splits}" )

    print( f"time_num {time_num} time_units {time_units}" )



device_list = [
		{ "name": "device_1", "tcpip": "192.168.0.209" },
		{ "name": "device_2", "tcpip": "192.168.0.92" },
		]


 #        self.probe_lists       = [ ( "192.168.0.",   0, 100 ),
for i_device in device_list:

    tcpip        = i_device[ "tcpip" ]
    splits       = tcpip.rsplit( ".",  1)
    tcpip_base   = splits[0]
    lo           = int( splits[1])
    hi           = lo + 1
    a_tuple      = ( tcpip_base, lo, hi )
    print( f"splits {splits}" )
    print( f"tcpip {tcpip}" )
    print( f"a_tuple {a_tuple}" )




