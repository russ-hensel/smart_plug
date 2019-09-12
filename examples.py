# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 09:30:09 2019

@author: russ
"""

import time
from pprint import pformat as pf

import pyHS100
from pyHS100 import Discover
import math

#  --------- Helper Function  -----
def dict_to_str( a_dict ):
        """
        works best on keys and values that are strings
        or use  pformat ( from pprint import pformat as pf )
        """
        info_str  = ""

        for key, value in list( a_dict.items()):
            if info_str == "":
                info_str +=  f"{key}:{value}"
            else:
                info_str +=  f"\n{key}:{value}"

        return info_str


#  --------- Helper Function  -----
def eval_it( eval_string ):
    print( f"Next eval the string {eval_string}" )
    eval( eval_string )
    # next is not really useful, eval returns None ( at least in some cases )
    # this next does run the code again in eval_string
    print(( eval_string, " => ", str( eval( eval_string )) ))

#  --------- Helper Function  -----
def get_tcpip(  ):
    tcpip   = "192.168.0.209"
    print( f"tcpip = {tcpip}" )
    return tcpip


# ----------------------------------------
def ex_discover():
    print( """
    ================ ex_discover():   ===============
    not working for me, may not try long enough, address by specifice address in
    functions below does work
    see code where this may be useful
    255.255.255.255 is a special broadcast address, which means "this network": it lets you send a
    broadcast packet to the network you're connected to, without actually caring about its address; in
     this, is similar to 127.0.0.1, which is a virtual address meaning "local host"

     are we using the right port  pyHS100 import Discover
      port: int = 9999,
    """ )
    device_values  = Discover.discover(timeout=100).values()  # are more arguments
    print( f"devices found: {len( device_values )}" )

    for dev in device_values:
        print(dev)
    print( "discover commplete" )


# in experiment found 0 but found with pyhs100 --host 192.168.0.209 --plug

#ex_discover()



# ----------------------------------------
def ex_sysinfo():
    print( """
    ================ ex_sysinfo():   ===============
    this gets all properties ?
    these anyway ( but perhaps as different types, or encoded )
    is_dimmable
    model
    has_emeter
    is_on
    led
    on_since
    """ )
    tcpip      = get_tcpip()
    plug       = pyHS100.SmartPlug( tcpip )

    sys_info   = plug.hw_info
    sys_info   =  plug.sys_info
    print( f"Hardware: {pf(sys_info)}")
    print( f"Full sysinfo: {pf(sys_info)}" ) # this prints lots of information about the device
    # these should be the same
    print( f"Full sysinfo: {pf(plug.get_sysinfo()) }" ) # this prints lots of information about the device


#ex_sysinfo()

# ----------------------------------------
def ex_misc_stuff():
    print( """
    ================ ex_misc_stuff():   ===============
    """ )

    tcpip   = get_tcpip()
    plug    = pyHS100.SmartPlug( tcpip )

#    print( f"Hardware: {pf(plug.hw_info)}")
#    print( f"Full sysinfo: {pf(plug.get_sysinfo()) }" ) # this prints lots of information about the device

#    print( f"Current state: {plug.state}" )
    print( f"Current is_on: {plug.is_on }" )

    plug.turn_off()
#    print( f"Current state: {plug.state}" )
    print( f"Current is_on: {plug.is_on }" )
    time.sleep( 2 )

    plug.turn_on()
#    print( f"Current state: {plug.state}" )
    print( f"Current is_on: {plug.is_on }" )
    time.sleep( 2 )


#    plug.state = "ON"
#    print( f"Current state: {plug.state}" )
#    time.sleep( 2 )
#
#    plug.state = "OFF"
#    print( f"Current state: {plug.state}" )

    # plug.state as read is depricated
    print( f"Current is_on: {plug.is_on }" )


    #Time information
    print( f"Current time: {plug.time}" )
    print( f"Timezone: {plug.timezone}" )

    print("Current consumption: %s" % plug.get_emeter_realtime())
    print("Per day: %s" % plug.get_emeter_daily(year=2016, month=12))
    print("Per month: %s" % plug.get_emeter_monthly(year=2016))



# ----------------------------------------
def ex_get_emeter_daily():
    print( """
    ================ ex_get_emeter_daily():   ===============
    data comes back for days with data
    """ )

    tcpip   = "192.168.0.209"
    plug    = pyHS100.SmartPlug( tcpip )
    a_dict  = plug.get_emeter_daily( year = 2019, month = 8 )
    msg     = f"get_emeter_daily {dict_to_str( a_dict )} "
    print( msg )

#    def get_emeter_daily(
#        self, year: int = None, month: int = None, kwh: bool = True
#    ) -> Dict:
    """Retrieve daily statistics for a given month.

    :param year: year for which to retrieve statistics (default: this year)
    :param month: month for which to retrieve statistics (default: this
                  month)
    :param kwh: return usage in kWh (default: True)
    :return: mapping of day of month to value
             None if device has no energy meter or error occurred
    :rtype: dict
    :raises SmartDeviceException: on error
    """

#ex_get_emeter_daily()


# ----------------------------------------
def ex_compute():
    print( """
    ================ ex_compute():   ===============

    """ )
    pass
#    print( f"side {(1/2)*math.sqrt(3.)}")

    d = 22.6
    print( f"radius { d /math.sqrt(3.)}")



ex_compute()