# -*- coding: utf-8 -*-

# parameters    for smart_plug and smart_plug_graph

import logging
import sys
import datetime
import os
import collections

#--------local imports
from   app_global import AppGlobal

class Parameters( object ):
    """
    sets parameter values, globally available thru AppGlobal
	users of this object should not change the values set here, treat as constants
	documentation of the parameters in the default mode subroutine: default_parms(  )
    """
    def __init__(self,  ):
        self.controller       = AppGlobal.controller   # set class property for global access to parameters

#        print( "define parameters" )
        SmartDevice = collections.namedtuple( 'SmartDevice', 'name tcpip more')

#        print( "set AppGlobal" )
        AppGlobal.parameters  = self    # this makes this instance globally available to the application
#        print( f"set global to {self}" )
#        print( f"set global to {AppGlobal.parameters}" )
        """
        parameters are set via subroutines that set a lot of values and most of these
        populate
        """
        self.default_parms()
        self.os_tweaks()
        self.computer_name_tweaks()

        #----------------- begin pick a mode --------------
        """
        modes set here override values in the default mode ( and in self.os_tweaks() self.computer_name_tweaks()   )
        """
        #self.mode_1()

        #----------------- end pick a mode ----------
        AppGlobal.device_list   = self.device_list
        #self.init_function_2    = None    # not needed or implemented

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of the default mode
        for particular operating systems
        """
        if  self.os_win:
            self.icon              = r"./green_house.ico"    #  default gui icon -- greenhouse this has issues on rasPi - need new icon for smartplug
            #self.icon              = None
        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_terminal_mode"
        for particular computers.  Put in settings for you computer if you wish
        """
        if self.computername == "smithers":
            self.port               = "COM5"   #  port not currently in use
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhouse":
            self.port               = "COM3"
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'
        elif self.computername == "theProf":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
        else:
            print( f"In parameters: no special settings for {self.computername}" )

    # -------
    def mode_1(self,  ):
        """
        yet to be defined, chnages only the name of the mode default
        """
        self.mode     = "Mode 1"

    # -------
    def default_parms(self,  ):
        """
        This sets all required ( and perhaps some unimplementd or left over ) values to a
        default value, good enough to run the application.
        This is also a primary location for the documentation of the values
        """
        self.mode               = "Default"    # name of the mode, displayed in the application title
        self.init_function_2    = None         # not used/useful as yet, a leftover

        self.db_file_name       = "test_data.db"   # file name for the sqlLite database

        #--------------- automatic settings -----------------
        self.our_os = sys.platform       #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"
        # print( "our_os is ", our_os )

        if self.our_os == "win32":
            self.os_win = True     # the OS is windows any version
        else:
            self.os_win = False    # the OS is not windows

        self.platform           = self.our_os    # I guess I had trouble deciding on a name -- I should eliminate one ......
        self.opening_dir        = os.getcwd()    # name of the directory that the application is started in. Probably "....../smart_plug
        self.computername       = os.getenv( "COMPUTERNAME" ).lower() # at least in windows the lower case name of your computer.  what in linux?

        #--------------- appearance ---------
        self.win_geometry      = '1300x700+20+20'    # window width x height + positionx + position y

        self.id_color          = "red"    # the application may have color to help identify it.  "blue"   "green"  and lots of other work
        self.id_height         = 20       # if there is an id pane, height of id pane, 0 for no pane

        # tkinter uses bg for background so I should probably make a global changee
        self.bkg_color         = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bkg_color         = "gray"   # override of above because I could
        self.bkg_color         = 'dark slate gray'
        self.btn_color         = "gray"   # color for buttons -- may not be implemented
        #self.btn_color         = "gray"   # color for buttons -- may not be implemented



        #------------------- devices ---------------------------
        """
		see documentatation at:  http://www.opencircuits.com/SmartPlug_Help_File#How_To:...   ( or in pdf file in this code distribution )
        note that this is a list of dictionaries, one dictionary for each device
		"""
#        self.device_list       =  [
#                { "name": "device_1",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },
#                { "name": "device_2",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },
#                { "name": "device_3",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },

        self.device_list       =  [
                { "name": "device_1",  "tcpip": "192.168.0.209",    },
                { "name": "device_2",  "tcpip": "192.168.0.209",    },
                { "name": "device_3",  "tcpip": "192.168.0.209",    },
                ]

        self.record_delta      = 10    # time in seconds between recordings -- global for all devices, ?? move to device list

        # ------------------- graphing
        """
        see   .prep_data()   selected_begin, data_begin, today_begin ...... for detail of some use
        not all may be implemented
        """
        # ---- next 4 parms are for the select clause -- may be changed in the GUI
        self.graph_begin_date     = datetime.date( 1981, 6, 16 )     # default beginning date for the sql select  ( year, month, day)
        self.graph_begin_date     = datetime.date( 2019, 8, 28 )     # override of above for no particular reason
        self.graph_end_date       = datetime.date( 2019, 9, 16 )     # default end date for the sql select  ( year, month, day)

        self.graph_begin_hr       = AppGlobal.dd_hours[0]          # default begin time for the sql select  (  index on 24 hr clock )
        self.graph_end_hr         = AppGlobal.dd_hours[0]          # default end time for the sql select  (  index on 24 hr clock )

        # ----- define the time labled 0 on the graph
        self.graph_time_zero    = "db_sql_begin"    #   time labled as 0 on the graph -- time in the sql begin
        self.graph_time_zero    = "data_begin"      #   time labled as 0 on the graph -- time for the first data point found

        self.graph_energy_zero  = "absolute" # "absolute" "first_value"

        # ----- graph time units
#        self.graph_time_units   = "days"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
#        self.graph_time_units   = "hour"  # time units used on graph
        self.graph_time_units   = "min"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
#        self.graph_time_units   = "sec"  # ??

        # size of the graph ( not data size, pixel size )
        self.graph_x_size  = 200
        self.graph_y_size  = 200

        # min/max inst power in watts
        self.graph_inst_power_min  = 0.
        self.graph_inst_power_max  = 100.

        # min/max total energy in KWatt * hr
        self.graph_total_power_min  = 0.00
        self.graph_total_power_max  =  .20

        self.graph_title     = "Smart Plug Power" # title used on the graph

        # -----  external exe and files  ----------------
        """
        name an editor for reading various test files, parameters.py, python log, and the help file.
        """
        self.ex_editor   =  r"leafpad"    # linux raspberry pi maybe
        if self.our_os == "win32":
            self.ex_editor   =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10
            self.ex_editor   =  r"C:\apps\Notepad++\notepad++.exe"    # russ theProf

        self.help_file       =  r"smart_plug_help.txt"

        # ----- logging ------------------
        # used by the python logger  -- controlls the  logging file
        self.logger_id          = "splug"
        self.pylogging_fn       = "smart_plug.py_log"     # file name for the python logging
        self.logging_level      = logging.DEBUG           #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        #self.logging_level     = logging.INFO            #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        self.print_to_log       = False                  # does what? not implemented

        self.log_gui_text       = True                  # True or False
        self.log_gui_text_level = logging.DEBUG         # if log_gui_text is True then this is the level that we log at

        # ----- message area in gui   -----------
        self.default_scroll     = 1        # 1 auto scroll the recieve area, else 0
        self.max_lines          = 1000

        # ------ timings for polling  may be some dead code
        self.gt_delta_t         = 100              # in ms --   lowest I have tried is 10 ms, could not see major cpu load
        self.ht_delta_t         = 1000/1000.      # helper thread timing this uses time so in seconds, convert to ms sorry for confusion

        self.queue_sleep         = .1  # see code ()   we pause for this period of time if the queue is full
        self.queue_length        = 20  # max length of queues communitating between threads

        self.prefix_info        = ">> "    # prefix for informational messages in the message area at bottom of gui ( if present )

        # ---- old ignore

#        self.graph_humid_max  = 100
#        self.graph_humid_min  = 0
#
#        self.graph_temp_min  = 0.
#        self.graph_temp_max  = 100.
#
#        # ---- old
#        self.graph_humid_max  = 100
#        self.graph_humid_min  = 0
#
#        self.graph_temp_min  = 0.
#        self.graph_temp_max  = 100.

    # ------------------------ make this select base on mode ------------
    def init_from_helper( self ):
         """
         call after helper is built
         not used at least yet
         """
         pass
         return

# ==============================================

# ========= threw error so commented out revisit later

#if __name__ == '__main__':
#    """
#    run the app here for convenience of launching
#    """
#    print( "" )
#    print( " ========== starting SmartPlug from parameters.py ==============" )
#
#    import smart_plug
#    a_app = smart_plug.SmartPlug(  )
# =================== eof ==============================










