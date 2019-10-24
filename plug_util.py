#!python3
# -*- coding: utf-8 -*-


"""
Purpose:



"""

#import logging
#import sys
#import os
#import time
#import datetime
#import traceback
#import queue
##import threading
#import importlib
import pyHS100
import collections
#
## ----------- local imports --------------------------
#import parameters
#import gui
#from   app_global import AppGlobal
#import smart_plug_helper
#import smart_plug_adapter

def call_msg_function( msg_function, msg ):
    #print( f"call_msg_function {msg}" )
    if msg_function is None:
        print( msg )
        return
    msg_function( msg )

# ----------------------------------------
def scan_a_plug(  tcpip, msg_function = None ):
    """
    scan a range of tcpip address for plugs
    scan_for_plugs( "192.168.0.", 209, 210, max_plugs = 0 ):
    msg_function   a function of one arg with a string as msg see call_msg_function ... None and it is ignored

    a plug is anything that responds to the plug protocol
    seems to take on order of 5 sec for each attempt that fails
    return list of tcpip address with plugs
    """
    ret      = False   # True if plug is found at the tcpip
    msg      = f"probe: {tcpip}"
    call_msg_function( msg_function, msg )
    try:
        plug            = pyHS100.SmartPlug( tcpip )
        info            = plug.hw_info
        ret             = True
    except pyHS100.smartdevice.SmartDeviceException  as exception:
        print( f"{type(exception )} {exception} " )
        msg         = f"failed to communicate with plug at {tcpip}"
        print( msg )
    return ret

# ----------------------------------------
def scan_for_plugs( start_tcpip, start_tcpip_ix, end_tcpip_ix, max_plugs = 0, msg_function = None ):
    """
    scan a range of tcpip address for plugs
    scan_for_plugs( "192.168.0.", 209, 210, max_plugs = 0 ):
    msg_function   a function of one arg with a string as msg see call_msg_function ... None and it is ignored

    a plug is anything that responds to the plug protocol
    seems to take on order of 5 sec for each attempt that fails
    return list of tcpip address with plugs
    could use function scan_a_plug but not really much code saved ??
    """
    found_list   = []
    for ix in range( start_tcpip_ix, end_tcpip_ix ):
        tcpip    = f"{start_tcpip}{ix}"
        msg      = f"probe: {tcpip}"
        call_msg_function( msg_function, msg )
        try:
            plug            = pyHS100.SmartPlug( tcpip )
            info            = plug.hw_info
            msg      = f"found device at: {tcpip}"
            call_msg_function( msg_function, msg )
            found_list.append( tcpip )

            if max_plugs == 0:
                continue
            if len( found_list )  >= max_plugs:
                break

#    #                print( msg  )
#                    AppGlobal.gui.print_info_string( msg )
        # may save event
#            full_info = "no info"
#            full_info = self.get_full_info( tcpip )
#            print( full_info )
        #except Exception as exception:             # look up correct exception
        except pyHS100.smartdevice.SmartDeviceException  as exception:
            print( f"{type(exception )} {exception} " )
            msg         = f"failed to communicate with plug at {tcpip}"
            print( msg )
            msg      = f"     no device at: {tcpip}"    # indented
            call_msg_function( msg_function, msg )
    return found_list

# ----------------------------------------
def get_full_info( tcpip ):
    """
    !! get info from a device
    return an ordered dict of all info we know how to get from device
    if device not found then will have full_info["device"]     = "failed to communicate" and length <= 3

    """
    #print("get_full_info")
    full_info              = {}
    full_info["tcpip"]     = tcpip
    try:
        plug                  = pyHS100.SmartPlug( tcpip )
        # some info may be duplicated but that just loweres efficiency

        # additional dicts
        add_dict              = plug.hw_info
        full_info.update( add_dict )

        full_info.update( plug.sys_info )
        full_info.update( plug.location )
        full_info.update( plug.timezone )

        # additional individual items
        full_info["alias"]                    = plug.alias
        full_info["device_type"]              = plug.device_type
        full_info["time"]                     = plug.time
        full_info["is_plug"]                  = plug.is_plug
        full_info["is_strip"]                 = plug.is_strip
        full_info["is_variable_color_temp"]   = plug.is_variable_color_temp
        full_info["is_bulb"]                  = plug.is_bulb

    except Exception as exception:             # look up correct exception
        pass   # point here is just to skip it
#        msg         = "full_info failed to communicate with plug"
#        print( f"type(exception ) {exception} " )
        full_info["device"]     = "failed to communicate"
        # log?
        #print( msg )
        #raise
    # consider a sort into an ordered dict
    #return full_info
    od = collections.OrderedDict( sorted( full_info.items(), key=lambda t: t[0] ))
    return od

#  ------------------ helper --------------------
def dict_to_str( a_dict ):
        """
        use for printing
        """
        info_str  = ""
        for key, value in a_dict.items():
            if info_str == "":
                info_str +=  f"{key}:{value}"
            else:
                info_str +=  f"\n{key}:{value}"

        return info_str

# ----------------------------------------
def test_stuff():
    """
    minimal, assumes at least one found
    """
    plug_list    = scan_for_plugs( "192.168.0.", 209, 211, max_plugs = 0 )
    print( plug_list )
    info    = get_full_info( plug_list[0] )
    print( info )
    print( dict_to_str( info ) )

# =======================================


if __name__ == '__main__':
        """
        see code
        """
        test_stuff()























