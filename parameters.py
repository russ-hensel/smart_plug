# -*- coding: utf-8 -*-

# parameters    for smart_plug



import logging
#import serial
import sys
import datetime
import os
import collections

#--------local
#import schedule_me
#import schedule_me_helper
from   app_global import AppGlobal

class Parameters( object ):
    """
    sets parameter values, globally available thru AppGlobal
    """
    def __init__(self,  ):
        self.controller       = AppGlobal.controller

#        print( "define parameters" )
        SmartDevice = collections.namedtuple( 'SmartDevice', 'name tcpip more')

#        print( "set AppGlobal" )
        AppGlobal.parameters  = self
#        print( f"set global to {self}" )
#        print( f"set global to {AppGlobal.parameters}" )

        self.default_parms()
        self.os_tweaks()
        self.computer_name_tweaks()   # or after mode set ??

        #----------------- pick a mode --------------
        self.mode_1()

        #----------------- end pick a mode ----------

        AppGlobal.device_list   = self.device_list
        self.init_function_2    = None

    # -------
    def os_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_terminal_mode"
        for particular operating systems
        """
        if  self.os_win:
            self.icon              = r"./green_house.ico"    #  greenhouse this has issues on rasPi
            #self.icon              = None                   #  default gui icon

        else:
            pass

    # -------
    def computer_name_tweaks( self ):
        """
        this is an subroutine to tweak the default settings of "default_terminal_mode"
        for particular computers.  Put in settings for you computer if you wish
        """

        if self.computername == "smithers":
            self.port               = "COM5"   #
            #self.port              = "COM3"   #
            self.win_geometry       = '1450x700+20+20'      # width x height position
            self.ex_editor          =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10 smithers

        elif self.computername == "millhouse":
            pass
            self.port               = "COM3"   #
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
            #self.win_geometry   = '1300x600+20+20'          # width x height position
        elif self.computername == "theProf":
            self.ex_editor          =  r"C:\apps\Notepad++\notepad++.exe"    # russ win 10 millhouse
        else:
            print( f"In parameters: no special settings for {self.computername}" )

    # -------
    def mode_1(self,  ):
        """
        yet to be defined, using default
        """
        self.mode     = "Mode 1"


    # -------
    def default_parms(self,  ):
        """
        """
        #--------------- for mode ---------
        self.mode               = "Default"
        self.init_function_2    = None

        self.db_file_name       = "test_data.db"

        #--------------- automatic -----------------
        self.our_os = sys.platform       #testing if our_os == "linux" or our_os == "linux2"  "darwin"  "win32"
        # print( "our_os is ", our_os )

        if self.our_os == "win32":
            self.os_win = True     # right now windows and everything like it
        else:
            self.os_win = False

        self.platform           = self.our_os    # sometimes it matters which os
        self.opening_dir        = os.getcwd()
        self.computername       = os.getenv( "COMPUTERNAME" ).lower() # what in linux

        # ================= sort these in


        #--------------- appearance ---------
        self.win_geometry      = '1300x700+20+20'    # width x height position

        self.id_color          = "red"    #  "blue"   "green"  and lots of other work
        self.id_height         = 20       # height of id pane, 0 for no pane
        self.id_color          = "green"
        self.bk_color          = "blue"   # color for the background, you can match the id color or use a neutral color like gray
        self.bk_color          = "gray"   #



        self.device_list       =  [
                { "name": "device_1",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },
                { "name": "device_2",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },
                { "name": "device_3",  "tcpip": "192.168.0.209", "more": None, "gui_label": None, "gui_combo": None  },
                                  ]

        self.record_delta      = 10    # time in seconds between recordings

        # ------------------- graphing

        # next 4 parms are for the select clause
        self.graph_begin_date     =    datetime.date( 1981, 6, 16 )
        self.graph_begin_date     =    datetime.date( 2019, 8, 28 )
        self.graph_end_date       =    datetime.date( 2019, 9, 16 )

        self.graph_begin_hr            = AppGlobal.dd_hours[0]  # index on 24 hr clock
        self.graph_end_hr              = AppGlobal.dd_hours[0]  #

        self.graph_time_zero    = "db_sql_begin"  #   time labled as 0 on the graph
        self.graph_time_zero    = "data_begin"  #   time labled as 0 on the graph
        """
        see   .prep_data()   selected_begin, data_begin, today_begin ...... not all may be implemented
        """

#self.graph_time_units   = "days"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
#        self.graph_time_units   = "hour"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
        self.graph_time_units   = "min"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
#        self.graph_time_units   = "days"  # ?? "hour" "min" .... add more   #  day hour  use my converter in future
#        self.graph_time_units   = "sec"  # ??
        """
        see   .prep_data()   sec, min, hr, day  and various spellings....

        """

        # size of the graph ( not data size, pixel size )
        self.graph_x_size  = 200
        self.graph_y_size  = 200

        # min max inst power in watts
        self.graph_inst_power_min  = 0.
        self.graph_inst_power_max  = 100.

        # min max total power in Kwatt * hr
        self.graph_total_power_min  = 0.00
        self.graph_total_power_max  =  .20


        self.graph_title     = "Smart Plug Power"

        # ---- old
        self.graph_humid_max  = 100
        self.graph_humid_min  = 0

        self.graph_temp_min  = 0.
        self.graph_temp_max  = 100.

        # ---- old
        self.graph_humid_max  = 100
        self.graph_humid_min  = 0

        self.graph_temp_min  = 0.
        self.graph_temp_max  = 100.

        # -----  external exe and files  ----------------
        self.ex_editor   =  r"leafpad"    # linux maybe
        if self.our_os == "win32":
            self.ex_editor   =  r"D:\apps\Notepad++\notepad++.exe"    # russ win 10
            self.ex_editor   =  r"C:\apps\Notepad++\notepad++.exe"    # russ theProf
        self.help_file       =  r"smart_plug_help.txt"

        #------------------- email
        self.email_to_address   = "russ_hensel@comcast.net"
        self.email_server       = "smtp.gmail.com"
        self.email_port         = 587

        self.email_from_address = "russ.hensel@gmail.com"
        self.email_account      = "russ.hensel@gmail.com"

        self.email_account_pass = "tentothe100!"

        self.email_min_repeat_time  = datetime.timedelta( days= 1, hours = 0, minutes = 1  )
        self.email_max_count    = 3


        #toaddr          = "squeakathighrant@gmail.com"

        #----------------- db connect in subroutines -- subroutines make it easire to switch sets of parameters

        #self.select_timedelat  = datetime.timedelta( days= 0, hours = 0, minutes = 30  )
        #self.dbRtoPi181( ")     # 181 is root cellar enviromental monitor


         # ----- logging ------------------
        # id used by the python logger  -- appears inside the logging file
        self.logger_id         = "splug"
        self.pylogging_fn      = "smart_plug.py_log"   # file name for the python logging
        self.logging_level     = logging.DEBUG           #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        #self.logging_level     = logging.INFO            #   CRITICAL	50   ERROR	40 WARNING	30  INFO	20 DEBUG	10 NOTSET	0
        self.print_to_log       = False                   # does what not implemented

        # ----- message area in gui   -----------
        self.default_scroll     = 1        # 1 auto scroll the recieve area, else 0
        self.max_lines          = 1000

        self.gt_delta_t         = 100              # in ms --   lowest I have tried is 10 ms, could not see cpu load

        self.ht_delta_t         = 1000/1000.      # helper thread timing this uses time so in seconds, convert to ms sorry for confusion

        self.queue_sleep         = .1
        self.queue_length        = 20

        self.prefix_info        = "# !!! "    # prefix for informational messages


    # ------------------------ make this select base on mode ------------
    def init_from_helper( self ):
         #def build_future_events( self ):
         """
         call after helper is built -- look at: ScheduleMeHelper.run() may move to restart??
         build the event here
         put in parameters, controller....... AppGlobal
         see event_list.run_event() to see how the functions are run
         """
         return
         # ------------------ old code





    # ------->> Parameter dicts   -- set up not tested

    #   ------------------------------------
    def create_parm_dict_greenhousexx( self, ):
        """
        parameters for the greenhouse event(s)
        """
        dict_name                       = "greenhouse"       # name for this in the dict of dictionaries
        a_dict                          = {}                 # empty dict

        a_dict["db_host"]               = '192.168.0.189'    # add the tcpip address of database server
        a_dict["db_port"]               = 3306               # database server port -- here default for mysql
        a_dict["db_db"]                 = 'pi_db'            # name of the database/schema

        a_dict["db_user"]               = 'pi_user'          # name of the database user
        a_dict["db_passwd"]             = 'taunot3point1fourpi'      # password for this user at this tcpip address

        # next the sql used to select from the database table
        a_dict["sql_select"]            = "SELECT ev_time, temp_1, humid_1 FROM ev_data           WHERE ( ev_time > %s ) order by temp_1 asc"


        a_dict["select_timedelat"]      = datetime.timedelta( days= 0, hours = 0, minutes = 30  ) # time used in the database select

        a_dict["alarm_min_temp"]        = 50        # ( farenheight ) used to set allarm ( email ) if temp gets too low
        a_dict["alarm_max_temp"]        = 75        # ( farenheight ) used to set allarm ( email ) if temp gets too high

        a_dict["failed_connect_count"]  = 0         # used as variable to count how many db connects in a row fail
        a_dict["max_connect_count"]     = 4         # at this number of faild connects an email is trigged
        a_dict["min_repeat_email_time"] = datetime.timedelta( days= 1, hours = 0, minutes = 0  )   # no emails repeated for this time period
        a_dict["time_last_email"]       = None      # time last email was sent

        AppGlobal.parameter_dicts[dict_name] = a_dict   # put in the AppGlobal dictionary








# ----------------------------

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartPlug from parameters.py ==============" )

    import smart_plug
    a_app = smart_plug.SmartPlug(  )


# =================== eof ==============================










