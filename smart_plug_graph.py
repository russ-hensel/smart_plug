# -*- coding: utf-8 -*-


"""
Purpose:
    smart plug_graph.py  ( tp link ) app with a gui for graphing and....
    related program smart_plug.py
    this is the main program, start it

Environment:
    development:
        Spyder 3.3.6
        Python 3.6
        Tkinker
        .....
    runtime:
        tested in Win 10 should work in all os's

"""

import logging
import importlib
import sys
import os
import time
#import traceback
import datetime
#import webbrowser
from   tkinter import messagebox
from   subprocess import Popen
#from   pathlib import Path
import psutil
import threading

# ----------- local imports --------------------------
import parameters
import gui_for_graph
#import gui_tabbed
from   app_global import AppGlobal
import graph_from_db
import define_db
import smart_plug_adapter


# ========================== Begin Class ================================
class SmartPlugGraph:
    """
    main and controller class for the SmartPlugGraph application
    see bottom of file for app startup
    """
    def __init__(self ):
        """
        """
        AppGlobal.main_thread_id   = threading.get_ident()
        # ------------------- basic setup --------------------------------
        print( "" )
        print( "=============== starting smart plug graph ========================= " )
        print( "" )

        self.app_name       = "SmartPlugGraph "
        self.version        = "Ver7 2019 11 06.2"
        self.gui            = None

        self.no_restarts    =  -1   # we count the restarts, adding one each time, first start is not a restart

        AppGlobal.controller = self
        AppGlobal.graph_app  = True
        self.restart( )

    # --------------------------------------------------------
    def restart(self ):
        """
        use to restart the app without shutting down first - it also called from __init__
        """
        self.no_restarts    +=  1
        if not( self.gui is None ):   # if gui root exists destroy it
             self.gui.root.destroy()
             importlib.reload( parameters )

        # ----- parameters
        self.parmeters_x    = "none"        # name without .py for parameters extension may be replaced by command line args
        self.get_args( )
        # command line might look like this
        # python smart_plug_graph.py    parameters=gh_paramaters

        self.parameters     = parameters.Parameters(  )  #  std name -- open early may effect other
        # AppGlobal.db_file_name       =  self.parameters.db_file_name  # or from init of parameters

        self.logger         = None      # set later none value protects against call against nothing
        if self.parmeters_x != "none":  # !! code clean up broke this, fixed ??
              self.parmeters_xx   =  self.create_class_from_strings( self.parmeters_x, "ParmetersXx" )
              self.parmeters_xx.modify( self.parameters )

        self.logger_id      = self.parameters.logger_id
        self.logger         = self._config_logger()
        AppGlobal.logger    = self.logger
        AppGlobal.logger_id = self.logger_id

        self.mode           = self.parameters.mode

        self.starting_dir   = os.getcwd()    # or perhaps parse out of command line
        self._prog_info()

        self.smartplug_adapter_list            = []
        for i_device in self.parameters.device_list:
            i_smartplug_adapter                = smart_plug_adapter.SmartPlugAdapter()
            self.smartplug_adapter_list.append( i_smartplug_adapter  )
            i_smartplug_adapter.name           = i_device[ "name" ]
            i_smartplug_adapter.tcpip          = i_device[ "tcpip" ]
            AppGlobal.smartplug_adapter_list   = self.smartplug_adapter_list

        self.grapher   = graph_from_db.Grapher()

        self.gui       = gui_for_graph.GUI( )  # create the gui or view part of the program
        # self.gui       = gui_tabbed.GUI( )  # create the gui or view part of the program  dropping this guy

        self.exception_records   = []          # keep a list of  ExceptionRecord  add at end limit    self.ex_max  ?? implemented?

        # now most of setupe memory has been allocated -- may want to chekc in again later, save this value ??
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"process memory = {mem_mega:10,.2f} mega bytes "
        print( msg )
        self.logger.log( AppGlobal.force_log_level,      msg )

        # --------------------------------------------------------
        self.gui.root.mainloop()

        self.grapher.end_graph()

        self.logger.info( self.app_name + ": all done" )
        return

    # --------------------------------------------------------
    def _config_logger( self, ):
        """
        configure the logger in usual way
        return: the logger
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )     # DEBUG , INFO    WARNING    ERROR    CRITICAL

        # create the logging file handler.....
        fh = logging.FileHandler(   self.parameters.pylogging_fn )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info("Done _config_logger") #  .debug   .info    .warn    .error

        return logger

     # -------------------------------------------------------
    def _prog_info( self ):
        """
        log info about program and its argument/environment
        after logger is set up
        """
        fll         = AppGlobal.force_log_level
        logger      = self.logger
        logger.log( fll,  "" )
        logger.log( fll,  "" )
        logger.log( fll,  "============================" )
        logger.log( fll,  "" )

        logger.log( fll, "Running " + self.app_name + " version = " + self.version + " Mode: " +self.parameters.mode )
        logger.log( fll,  "" )

        if len( sys.argv ) == 0:
            logger.log( fll, "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                logger.log( fll, "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        logger.log( fll,  "current directory " +  os.getcwd() )
        logger.log( fll,  "COMPUTERNAME "      +  os.getenv( "COMPUTERNAME" ) )

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        logger.log( fll, "Time now: " + string_rep )
        return

    #----------------------------------------------
    def get_args( self, ):
        """
        left over may implement or not
        get the argument off the command line
        no spaces allowed around the = sign
        note log file not yet open?
        """
        for iarg in sys.argv[1:]:
            #print iarg
            argsplits   = iarg.split("=")
            parm_name   = argsplits[0]
            parm_value  = argsplits[1]
            #print argsplits

            # so far only one is captured
            if parm_name == "parameters":
                self.parmeters_x  =  parm_value   #
                print( "command line arg >> " + iarg  )  # log file not open
            else:
                print( "no parameter extensions" )
            return

    # -------------------------------------------------------
    def create_class_from_strings( self, module_name, class_name):
        """
        left over code, delete later
        this will load a class from string names
        this makes it easier to specify classes in the parameter file.
        believe it is used for both the comm drive and the "processor"
        args:  strings
        ret:   instance of the class
        """
        if not( self.logger is None ):
            self.logger.debug(  "create class "  +  module_name +  " " +  class_name )

        a_class    = getattr(importlib.import_module(module_name), class_name)
        instance   = a_class(  )
        return instance

    # -------------------------------------------------------
    def polling( self, ):
        """
        currently no polling, probably not called
        used if I multi-thread the app.
        """
        pass

    # ----------------------------------------------
    def back_sundays_from_now( self, n_sun ):
        """
        n_sun back, 1 is lowest legal
        from now - might be good
        return: datetime
        """
        #rint( "----------- back_sundays  ------------" )
        dt       = datetime.datetime.now()
        tt       = dt.timetuple()
        dow      = tt[6]
        y, m, d  = tt[0:3]

        dt_midnight   =  datetime.date( y, m, d )
        #print dt_midnight

        midnight_sun   =  dt_midnight - datetime.timedelta( days = (  ( n_sun - 1 ) * 7 ) + 1 + dow  ) #- 6 - dow  ) )
        return midnight_sun

    #-------------------------------------------
    def db_select_from_now_minus_hr( self, n_hr ):
        """
        put values into gui for later use in graph
        need date for calendar
        need index for hour
                self.gui.cal_begin
                self.gui.cal_end

                will move forward an hour and backward an hour then truncate
        """
#        msg   = "db_select_from_now_minus_hr not implemented"
#        print( msg )
#        AppGlobal.gui.display_info_string( msg )

        delta_hr        = datetime.timedelta( hours =1 )
        dt              = datetime.datetime.now()
        dt_end          = dt + delta_hr
        dt_begin        = dt - delta_hr

        date_begin      = dt_begin.date()
        self.gui.cal_begin.set_date( date_begin )
        hr_begin        = dt_begin.hour
        self.gui.time_begin.set( AppGlobal.dd_hours[ hr_begin -1 ] )

        date_end      = dt_end.date()
        self.gui.cal_end.set_date( date_end )
        hr_end        = dt_end.hour
        self.gui.time_end.set( AppGlobal.dd_hours[ hr_end -1 ] )


#        print( f"datetime.datetime.now() = {dt}" )

        #ix_hr              = hr_begin - 2   # will it be an int think this is safe  no use deltas


#        print(( 'year  :     ', dt.year   ))   # all attributes may not exist so may need try except
#        print( f"month :     {dt.month}"   )   # all
#        print(( 'hour  :     ', dt.hour   ))
#        print(( 'minute:     ', dt.minute ))
#        print(( 'second:     ', dt.second ))
#        print(( 'microsecond:', dt.microsecond ))
#        print(( 'tzinfo:     ', dt.tzinfo ))

#        dt     = datetime.datetime.now()
#        print(( "datetime.datetime.now() = ", dt ))
#
#        # this a date, not a datetime
#        dt      = datetime.date( 1981, 6, 16 )
#        print(( f"datetime.date( 1981, 6, 16 ) = {type(dt)} {dt}", dt ))
#
#        dt      = datetime.datetime( 2008, 11, 10, 17, 53, 59 )
#        print(( "datetime( 2008, 11, 10, 17, 53, 59 ) = ", dt ))
#

    #-------------------------------------------
    def db_select_today( self, ):
        """
        what it says
        put values into gui for later use in graph

        """
        #print( "db_select_today" )
        dt_now         = datetime.datetime.now()
        tt_now         = dt_now.timetuple( )
        dt_now         = datetime.datetime.now()

        # set to begin today
        date_begin     =  dt_now.date()  # today
        self.gui.cal_begin.set_date( date_begin )                           # actually could just use the datetime
        self.gui.time_begin.set( AppGlobal.dd_hours[0] )

        # set to begin tomorrow, end today
        date_end     =  ( dt_now + datetime.timedelta( days=1 ) ).date()  #
        self.gui.cal_end.set_date( date_end )                               # actually could just use the datetime
        self.gui.time_end.set( AppGlobal.dd_hours[0] )

    #-------------------------------------------
    def db_select_from_now( self, n_days ):
        """
        update in process this as test of gui_for_graph

        get now, split to date and time of day,  round time of day forward, adjust date if required.
        subtract time from now and round backward to get new date and time of day
        convert times into strings and place in the gui
        look at conversions for query in... gui.get_begin_end  ... and maybe some of this logic should be in the gui as well

        select with start now  and  n days  back )
        need to set self.db_start and self.db_end
        note formats dt for date time and ts for time stamp
        does not seem to round time to begin of day should it ??
        """
        pass
        #print( "----------- db_select_from_sun  ------------" )
#        dt       = datetime.datetime.now()
#        # convert to string  and timestamp store both
#        a_string        = dt.strftime( "%Y/%m/%d" )    # not quite accurate, add formatting
#        ts_end          = time.mktime( dt.timetuple() )
#
#        self.db_end     = ( a_string, ts_end )
#
#        dt              = datetime.datetime.now()
#        dt              = dt - datetime.timedelta( days = 1 * n_days )   #this seems to mess up next line
#
#        a_string        = dt.strftime( "%Y/%m/%d" )
#        ts_begin        = time.mktime( dt.timetuple() )
#
#        self.db_start   = ( a_string, ts_begin )
#        self.display_db_select()

    #-------------------------------------------
    def db_select_from_sun( self, n ):
        """
        select with start date going back n sundays )
        """
        #print( "----------- db_select_from_sun  ------------" )

        dt       = datetime.datetime.now()
        # need to add a day, or will end at begin of day
        dt       =  dt + datetime.timedelta( days = 1  )

        tt       = dt.timetuple()     # but what time zone
        dow      = tt[6]
        y, m, d  = tt[0:3]

        # convert to string  and timestamp store both
        a_string  = dt.strftime( "%Y/%m/%d" )
        ts        = time.mktime( dt.timetuple() )

        self.db_end   = ( a_string, ts )

        dt       = self.back_sundays_from_now( n )
        #dt       = datetime.datetime.now()
        tt       = dt.timetuple()
        dow      = tt[6]
        y, m, d  = tt[0:3]

        # convert to string  and timestamp store both
        a_string  = dt.strftime( "%Y/%m/%d" )
        ts        = time.mktime( dt.timetuple() )

        self.db_start   = ( a_string, ts )
        self.display_db_select()

    #-------------------------------------------
    def db_select_from_parms( self ):
        """
        what it says
        """
        self.gui.cal_begin.set_date( self.parameters.graph_begin_date  )
        self.gui.cal_end.set_date( self.parameters.graph_end_date  )

        self.gui.time_begin.set( self.parameters.graph_begin_hr )
        self.gui.time_end.set( self.parameters.graph_end_hr )

    #-------------------------------------------
    def display_db_select( self ):
        """
        !! fix allignment of lables and length and will not need padding
        """
        spacer   = "                                              "
        lab_len  = 20

        lbl_text  = ( "Start: " + self.db_start[0] + spacer )[0:lab_len]
        self.gui.lbl_start.config(  text    =  lbl_text     )

        lbl_text  = ( "End:   " + self.db_end[0]   + spacer )[0:lab_len]
        self.gui.lbl_end.config(    text    =  lbl_text     )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        callback from gui button
        """
        AppGlobal.os_open_txt_file( self.parameters.pylogging_fn )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        callback from gui button
        """
        a_filename  = self.starting_dir  + os.path.sep + "parameters.py"
        AppGlobal.os_open_txt_file( a_filename )

    # ----------------------------------------------
    def os_open_parmxfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + self.parmeters_x + ".py"
        AppGlobal.os_open_txt_file( a_filename )

    # ----------------------------------------------
    def os_open_helpfile( self,  ):
        """
        callback from gui button

        """
        help_file            = self.parameters.help_file
        AppGlobal.os_open_help_file( help_file )

    # ------------------ callbacks for buttons -----------------
    def cb_graph( self,  ):
        """
        callback from gui button
        do the graph -- called from gui send to grapher
        need !! to fix point count across multiple graphs and getting rid or point cache
        """
        #self.grapher.do_graph( self.db_start, self.db_end  )  from smart terminal
        # move get date back to here
        ( ts_begin, ts_end  ) = AppGlobal.gui.get_begin_end()
        print( ts_begin, ts_end )
        msg    = "Beginning a graph..."
        AppGlobal.gui.display_info_string( msg )
        # !! get device from the gui
        device_list   = self.gui.get_checked_device_adapters()
        d_len         = len( device_list )
        if  d_len == 0:
           msg    = "No devices selected, so no graph."
           AppGlobal.gui.display_info_string( msg )
           return
        self.grapher.do_graph( device_list, ts_begin, ts_end  )

    # ----------------------------------------------
    def cb_rb_select( self,  ):
        """
        call back for gui button  -- still thinking about these
        """
        ix_rb     = self.gui.rb_var.get()
#        print( "rb val", ix_rb )

        if    ix_rb == 0:
            self.db_select_from_parms()
        elif  ix_rb == 1:
            self.db_select_today()
        elif  ix_rb == 2:
            self.db_select_from_sun( 2 )

#        elif  ix_rb == 6:
#            self.db_select_from_now( 1 )
        elif  ix_rb == 6:
            self.db_select_from_now_minus_hr( 1 )
        elif  ix_rb == 7:
            self.db_select_from_now( 7 )
        else:
            self.db_select_from_sun( ix_rb )

    # ----------------------------------------------
    def cb_define_db( self,  ):
        """
        define a new sql data base file
        must be in a new file ( not currently existing )
        """
        db_file_name    = AppGlobal.gui.get_db_file_name()   # !! may want to change to use a dialog
        if os.path.isfile( db_file_name ):
#            msg   =  f"File exists: {db_file_name}"
#            AppGlobal.gui.display_info_string( msg )
#            print( f"file exists: {db_file_name}" )
            msg   =  f"Error: File ({db_file_name}) already exists."
            AppGlobal.gui.display_info_string( msg )
            messagebox.showinfo( "Error", msg )
            return
        msg     = f"Creating empty database in file ({db_file_name})."
        AppGlobal.gui.display_info_string( msg )
        define_db.create_db( db_file_name )
        msg     = f"Empty database in file ({db_file_name}) done."
        AppGlobal.gui.display_info_string( msg )

 # ----------------------------------------------
    def cb_export_csv( self,  ):
        """
        call back for gui button !! need to make like graph and send a list of adapters ... in process
        """
        print("cb_export_csv  ")
        device_list   = self.gui.get_checked_device_adapters()
#        print( device_list )
        d_len         = len( device_list )
        if  d_len == 0:
           msg    = "No devices selected, so no CSV output."
           AppGlobal.gui.display_info_string( msg )
           return

        ( ts_begin, ts_end  ) = AppGlobal.gui.get_begin_end()
        print( f"timestamps for csv {ts_begin}, {ts_end}" )
        self.grapher.export_csv( device_list, ts_begin, ts_end  )

 # ----------------------------------------------
    def cb_test( self,  ):
        """
        call back for gui button
        """
        print("cb_test called may cause error if test not set up  ")

    # ----------------------------------------------
    def cb_about( self,  ):
        """
        call back for gui button
        """
        AppGlobal.about()

# --------------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        a_app = SmartPlugGraph(  )


# ====================== eof ========================



