# -*- coding: utf-8 -*-

"""
Purpose:
parameters    for smart_plug and smart_plug_graph

    Also documents the meaning of the parameters ( hopefully ).
    If you are changing parameters read the code first


"""

import logging
import sys
import datetime
import os
import collections

#--------local imports
from   app_global import AppGlobal

class Parameters( object ):
    """
    sets parameter values, globally available through AppGlobal
	outside code using this object this object should not change the values set here, treat as constants

	documentation of the parameters can be found in this code particurlally in the default mode subroutine: default_parms(  )
    """
    def __init__(self,  ):
        self.controller       = AppGlobal.controller   # set class property for global access to parameters

        SmartDevice = collections.namedtuple( 'SmartDevice', 'name tcpip more')

        AppGlobal.parameters  = self    # this makes this instance globally available to the application

        """
        parameters are set via subroutines that set a lot of values at one shot
        """
        self.default_parms()
        self.os_tweaks()
        self.computer_name_tweaks()

        #----------------- begin pick a mode --------------
        """
        modes set here override values in the default mode ( and in self.os_tweaks() self.computer_name_tweaks()   )
        mode_1, mode_2 are provided as a place holders
        """
        self.mode_1()     # placeholde mode
#        self.mode_2()     # placeholde mode
        #----------------- end pick a mode ----------
        AppGlobal.device_list   = self.device_list    # does not seem necessary, consider removal


    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of the default mode
        for particular operating systems
        """
        if  self.os_win:
            pass
            #self.icon              = r"./green_house.ico"    #  default gui icon -- greenhouse this has issues on rasPi - need new icon for smartplug
            #self.icon              = None
        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_parms mode = Default"
        for particular computers.  Put in settings for you computer if you wish
        smithers, millhouse, the_prof, are all computers belonging to russ
        """
        if self.computername == "smithers":
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers
            self.db_file_name       =  "smithers_db.db"

        elif self.computername == "millhouse":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            #self.win_geometry   = '1300x600+20+20'
            self.db_file_name       =  "millhouse_db.db"

        elif self.computername == "theprof":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"
            self.db_file_name       =  "the_prof_db.db"
        else:
            print( f"In parameters: no special settings for {self.computername}" )

    # -------
    def mode_1(self,  ):
        """
        changes only the name of the mode and...  Largely a place holder
        """
        self.mode               = "Mode 1"
        self.graph_time_units   = "days"  # ?? "hour" "min" days seconds.... add more   #  day hour  use my converter in future

    # -------
    def mode_2(self,  ):
        """
        changes only the name of the mode and...  Largely a place holder
        """
        self.mode               = "Mode 2"

    # -------
    def default_parms(self,  ):
        """
        This sets all required ( and perhaps some unimplemented or left over ) values to a
        default value, good enough to run the application.
        This is also a primary location for the documentation of the values
        """
        self.mode               = "Default"    # name of the mode, displayed in the application title

        # ----- icons for the apps
        # I have only made icons for windows most of these were for testing
        # self.icon is for smart_plug
        self.icon               = "./spark_plug.ico"   # use None for no icon
        self.icon               = "./spark_plug_white.ico"
        self.icon               = "./electrical_plug_white_bkg.ico"
        # self.icon_graph is for smart_plug_graph
        self.icon_graph         = "./spark_plug_white.ico"         # since we are supporting 2 apps in this parameter file

        self.init_function_2    = None             # not used/useful as yet, a leftover

        self.db_file_name       = "test_data.db"   # file name for the sqlLite database -- this is default, use the one in app global

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
        self.win_geometry      = '1300x700+20+20'    # window width x height + position x + position y

        self.id_color          = "red"    # the application may have color to help identify the gui. think dead code  "blue"   "green"  and lots of other work
        self.id_height         = 20       # if there is an id pane, height of id pane, 0 for no pane

        # tkinter uses bg for background so I should probably make a global change
        self.bkg_color         = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bkg_color         = "gray"   # override of above because I could
        self.bkg_color         = 'dark slate gray'
        self.bn_color          = "gray"   # color for buttons -- may not be implemented -- use bn to match tkinter api
        self.btn_color         = self.bn_color

        #------------------- devices ---------------------------
        """
        this identifies the smart plugs -- must configure this to talk to your devices
		see documentation at:  http://www.opencircuits.com/SmartPlug_Help_File#How_To:...   ( or in pdf file in this code distribution )
        note that this is a list of dictionaries, one dictionary for each device

        name: your name for the device, may match the alias or not ( what you named the plug in its setup )
              name is what shows on the gui, and is the id in the database file, keep fairly short
        tcpip:  the tcpip address of your device -- see help file for info on how to determine this
        delta_t: how often the device should be monitored
        ..... planning to add more like location and purpose ??

        plug has some additional "built in atributes", you can see them after you connect by press the smart_plug gui butto with the device name
        the information is displayed in the message areas of the gui
		"""
        # list of dictionaries
        self.device_list       =  [
                { "name": "device_1",    "tcpip": "192.168.0.209", "delta_t": 10,   },
                { "name": "device_209",  "tcpip": "192.168.0.209", "delta_t": 10,   },
                { "name": "device_210",  "tcpip": "192.168.0.210", "delta_t": 10,   },
                ]

        # since this is python only this setting sticks
        self.device_list = [
                              { "name": "device_1", "tcpip": "192.168.0.209", "delta_t": 10,   },
                              { "name": "device_2", "tcpip": "192.168.0.92",  "delta_t": 10,   },
                            ]
        """
        !! note to russ
		revise output to match above
		>> self.device_list = [
		{ "name": "device_1", "tcpip": "192.168.0.209" },
		{ "name": "device_2", "tcpip": "192.168.0.92" },
		]
        """

        """
        probe for devices smart_plug gui <probe plugs> is an appliction feature that will look for plugs and output
        to the message area a setting for device_list that will connect to the devices it finds
        looking for devices takes seconds for each address checked so can be slow
        """

        #list of tuples to be probed to find plugs  base, low_index hi_index hi not inclusive
        self.probe_lists       = [ ( "192.168.0.", 209, 210 ),
                                                               ]  # this will check 192.168.0.209


#        #list of tuples to be probed to find plugs  base, low_index hi_index hi not inclusive
#        self.probe_lists       = [ ( "192.168.0.", 209, 250 ),
#                                   ( "192.168.0.",  50, 200 ),   ]
#
#
#        # pretty much everything  will probably take a long time
#        self.probe_lists       = [ ( "192.168.0.",   0, 100 ),
#                                    ( "192.168.0.", 100, 254 ),   ]
#

        # next setting will cause the <probe plug> to stop probing when this number of plugs is found
        self.max_probe         = 2   # 0 is unlimited -- when looking probe/scan stop at this limit

        self.record_delta      = 10  # time in seconds between recordings -- global for all devices, ?? move to device list time used for monitor as well

        # ------------------- graphing from db
        """
        see   .prep_data()   selected_begin, data_begin, today_begin ...... for detail of some use
        not all may be implemented
        """
        # ---- next 4 parms are for the select clause -- may be changed in the GUI
        self.graph_begin_date     = datetime.date( 1981, 6,  16 )    # default beginning date for the sql select  ( year, month, day)
        self.graph_begin_date     = datetime.date( 2019, 10, 10 )    # override of above for no particular reason
        self.graph_end_date       = datetime.date( 2019, 11, 20 )    # default end date for the sql select  ( year, month, day)

        self.graph_begin_hr       = AppGlobal.dd_hours[0]            # default begin time for the sql select  (  index on 24 hr clock )
        self.graph_end_hr         = AppGlobal.dd_hours[0]            # default end time for the sql select    (  index on 24 hr clock )

        # ----- define setup for db graph
        self.graph_db_time_zero    = "data_begin"    #  "db_sql_begin"  "data_begin" "begin_today" time labeled as 0 on the graph -- see xxx.py
        self.graph_db_time_units   = "days"  #  "seconds."  "min" "hour"  "days" ... add more ??


        self.graph_db_energy_zero  = "absolute" # "absolute" "first_value"

        # ----- define setup for live graph

        self.graph_live_time_units   = "min"  # ?? "hour" "min" days seconds.... add more   #  day hour  use my converter in future
        self.graph_live_time_zero    = "now"    #   time labeled as 0 on the graph


        # size of the graph think currently shared between live and db ( not data size, pixel size )  belive in "inches"
        self.graph_x_size  = 3
        self.graph_y_size  = 3

        self.graph_x_size  = 2.5
        self.graph_y_size  = 2.5

		# next consider live and db and add some sort of auto scaling

        # min/max inst power in watts
        self.graph_inst_power_min  = 0.
        self.graph_inst_power_max  = 2000.

        # min/max total energy in KWatt * hr
        self.graph_total_energy_min  = 0.00
        self.graph_total_energy_max  = 1000.   # .20

        self.graph_title     = "Smart Plug Power" # title used on the graph

        # -----  external exe and files  ----------------
        """
        name an editor for reading various test files, parameters.py, python log, and the help file.
        """
        self.ex_editor   =  r"leafpad"    # linux raspberry pi maybe
        if self.our_os == "win32":
            self.ex_editor   =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10
            self.ex_editor   =  r"C:\apps\Notepad++\notepad++.exe"    # russ theProf

        # help file can be web ( open with browser ), or txt ( open with self.editor ) or anything else ( will try to shell out may or may not work )
        self.help_file       =  r"help.txt"
        self.help_file       =  "http://www.opencircuits.com/SmartPlug_Help_File"   # can be url or a local file

#        self.help_file       =  "./wiki_etc/SmartPlugHelpFile-OpenCircuits.pdf"
#        self.help_file       =  r"D:\Russ\0000\python00\python3\_projects\smart_plug\Ver6\wiki_etc\SmartPlugHelpFile-OpenCircuits.pdf"

        # ----- logging ------------------
        # used by the python logger  -- controls the  logging file
        self.logger_id          = "splug"
        self.pylogging_fn       = "smart_plug.py_log"     # file name for the python logging
        self.logging_level      = logging.DEBUG           #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        #self.logging_level     = logging.INFO            #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        self.print_to_log       = False                   # does what? not implemented

        self.log_gui_text       = True                    # True or False   implemented ??
        self.log_gui_text_level = logging.DEBUG           # if log_gui_text is True then this is the level that we log at

        # override whatever you want
        if  AppGlobal.graph_app:
            self.pylogging_fn       = "smart_plug_graph.py_log"     # file name for the python logging
            self.logging_level      = logging.INFO          #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0

        # ----- message area in gui   -----------
        self.default_scroll     = 1        # 1 auto scroll the receive area, else 0
        self.max_lines          = 1000

        # ------ timings for polling  may be some dead code
        self.gt_delta_t         = 100              # in ms --   lowest I have tried is 10 ms, could not see major cpu load
        self.ht_delta_t         = 100/1000.       # helper thread timing this uses time so in seconds, convert to ms sorry for confusion

        self.queue_sleep         = .1  # see code ()   we pause for this period of time if the queue is full
        self.queue_length        = 20  # max length of queues communicating between threads

        self.prefix_info        = ">> "    # prefix for informational messages in the message area at bottom of gui

        # ---- old dead ignore ( but may rise from dead )

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


# =======================================

if __name__ == '__main__':
    """
    run the app -- this may be old code, check that it is right against main app
    """
    import smart_plug
    a_app = smart_plug.SmartPlug(  )








