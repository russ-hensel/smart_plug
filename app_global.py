# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 21:06:50 2017

@author: Russ
"""
#typical use
#from app_global import AppGlobal
#
#self.parameters    = AppGlobal.parameters

import sys


class AppGlobal( object ):
    """
    use at class level ( do not _init_ ) for applicaation globals, similar to but different from parameters
    some global functions ??
    """
    force_log_level         = 99    # value to force logging, high but not for errors

    controller              = None      # populated by the controller
    parameters              = "None"    # populated by parameters
    gui                     = None      # populsted by the gui
    logger                  = None# populated by the controller
    logger_id               = None# populated by the controller
    scheduled_event_list    = "None"
    helper                  = "None"
    parameter_dicts         = {}         # set up in parameters ????? -- see and example std setup somw where
    smartplug_adapter_list   = None    # from controlerself.smartplug_adapter_list

    dd_hours    = [ "0 Begin Day","01 - 1am","02 2am","03 3am","04 4am","05 5am","06 6am","07 7am","08 8am","09 9am","10 10am","11 11am","12 12am Noon",
                             "13 - 1pm","14 2pm","15 3pm","16 4pm","17 5pm","18 6pm","19 7pm","20 8pm","21 9pm","22 10pm","23 11pm",  ]



    def __init__(self,  controller  ):
        # this guy should not be created
        pass

     # ----------------- debuging ----------------
    def to_str():
        """
        convert some of AppGlobals contents to a string for debugging - left over from some other app
        """
        a_string   = (   "AppGlobal" +
                                  str (AppGlobal.parameter_dicts ) +
                           "\n    ---------- greenhouse ----------\n" + str( AppGlobal.parameter_dicts["greenhouse"]) +
                           "\n    ---------- rootcellar ----------\n" + str( AppGlobal.parameter_dicts["rootcellar"])     )
        return a_string

    def print_me():
         sys.stdout.flush()
         print("========== AppGlobal =================")
         print( AppGlobal.to_str( ) )
         sys.stdout.flush()


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
#    print( "" )
#    print( " ========== starting ScheduleMe from sch_me.py ==============" )
#    import schedule_me
#    a_app = schedule_me.ScheduleMe(  )



# ======================== eof ======================