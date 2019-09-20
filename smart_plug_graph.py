# -*- coding: utf-8 -*-

# main for smartplug
# for documentation see: *>text
"""

Purpose:
    smart plug_graph.py  ( tp link ) app with a gui for graphing and....
    related program smart_plug.py
    this is the main program, start it

Environment:

        Spyder 3.3.6
        Python 3.6
        Tkinker
        .....
        tested in Win 10 should work in all os's

"""

import logging
import importlib
import sys
import os
import time
#import traceback
import datetime

# ----------- local imports --------------------------
import parameters
import gui_for_graph
#import gui_tabbed
from   app_global import AppGlobal
import graph_smart_plug
import define_db
import smart_plug_adapter

          # this may need refactoring but for now.....

# ========================== Begin Class ================================
class SmartPlugGraph:
    """
    main and controller class for the SmartPlugGraph application
    see bottom of file for app startup
    """
    def __init__(self ):
        """
        """
        # ------------------- basic setup --------------------------------
        print( "" )
        print( "=============== starting smart plug graph ========================= " )
        print( "" )

        self.app_name       = "SmartPlugGraph "
        self.version        = "Ver5 2019 09 19.0"
        self.gui            = None

        self.no_restarts    =  -1   # we count the restarts, adding one each time, first start is not a restart

        AppGlobal.controller = self
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
        # python smart_terminal_graph.py    parameters=gh_paramaters

        self.parameters     = parameters.Parameters(  )  #  std name -- open early may effect other

        self.logger         = None      # set later none value protects against call against nothing
        if self.parmeters_x != "none":  # !! code clean up broke this, fixed ??
              self.parmeters_xx   =  self.create_class_from_strings( self.parmeters_x, "ParmetersXx" )
              self.parmeters_xx.modify( self.parameters )

        self.logger_id      = self.parameters.logger_id
        self.logger         = self._config_logger()
        AppGlobal.logger    = self.logger
        AppGlobal.logger_id = self.logger_id

        self.db             = None

        #self.connect        = self.parameters.connect
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

        self.grapher   = graph_smart_plug.Grapher()

        self.gui       = gui_for_graph.GUI( )  # create the gui or view part of the program
        # self.gui       = gui_tabbed.GUI( )  # create the gui or view part of the program  dropping this guy

        self.exception_records   = []          # keep a list of  ExceptionRecord  add at end limit    self.ex_max  ?? implemented?

        self.display_db_status()
        #self.db_select_from_parms()

        # --------------------------------------------------------
        self.gui.root.mainloop()

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
        log info about program and its argument/enviroment
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
        # !! add mode

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
                print( "no parmeter extensions" )
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
        used if I multithread the app.
        """
        pass

    # ----------------------------------------------
    def back_sundays_from_now( self, n_sun ):
        """
        n_sun back, 1 is lowest leagal
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
    def db_select_from_now( self, n_days ):
        """
        select with start now  and  n days  back )
        need to set self.db_start and self.db_end
        note formats dt for date time and ts for time stamp
        does not seem to round time to begin of day should it ??
        """
        #print( "----------- db_select_from_sun  ------------" )
        dt       = datetime.datetime.now()
        # convert to string  and timestamp store both
        a_string        = dt.strftime( "%Y/%m/%d" )    # not quite accurate, add formatting
        ts_end          = time.mktime( dt.timetuple() )

        self.db_end     = ( a_string, ts_end )

        dt              = datetime.datetime.now()
        dt              = dt - datetime.timedelta( days = 1 * n_days )   #this seems to mess up next line

        a_string        = dt.strftime( "%Y/%m/%d" )
        ts_begin        = time.mktime( dt.timetuple() )

        self.db_start   = ( a_string, ts_begin )
        self.display_db_select()

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

        """

        print( "fix db_select_from_parms" )
#        time_str   =  self.parameters.graph_start_time
#        time_ts    =  time.mktime( datetime.datetime.strptime( time_str, "%Y/%m/%d").timetuple() )
#
#        self.db_start   = ( time_str, time_ts )
#
#        time_str   =  self.parameters.graph_end_time
#        time_ts    =  time.mktime( datetime.datetime.strptime( time_str, "%Y/%m/%d").timetuple() )
#        self.db_end     = ( time_str, time_ts )
#        self.display_db_select()

    #-------------------------------------------
    def display_db_select( self ):

        spacer   = "                                              "
        lab_len  = 20

        lbl_text  = ( "Start: " + self.db_start[0] + spacer )[0:lab_len]
        self.gui.lbl_start.config(  text    =  lbl_text     )

        lbl_text  = ( "End:   " + self.db_end[0]   + spacer )[0:lab_len]
        self.gui.lbl_end.config(    text    =  lbl_text     )

    #-------------------------------------------
    def display_db_status( self ):
        """
        was used for marina sql
        """
        pass
#        spacer   = "                                              "
#        lab_len  = 25
#        if self.db is None:
#            lbl_text  = ( "Status: Not Connected" + spacer )[0:lab_len]
#            self.gui.lbl_db_status.config(  text    =  lbl_text     )
#
#            lbl_text  = ( "Host: None" + spacer )[0:lab_len]
#            self.gui.lbl_db_host.config(    text    =  lbl_text     )
#
#            lbl_text  = ( "DB: None" + spacer )[0:lab_len]
#            self.gui.lbl_db_db.config(      text    =  lbl_text     )
#
#            lbl_text  = ( "User: None" + spacer )[0:lab_len]
#            self.gui.lbl_db_user.config( text       =  lbl_text     )
#
#        else:
#            lbl_text  = ( self.parameters.connect    + spacer )[0:lab_len]
#            self.gui.lbl_db_connect.config(    text    =  lbl_text     )
#
#            if self.db.db_open:
#                is_open = "Open"
#            else:
#                is_open = "Closed"
#
#            lbl_text  = ( "Status: " + is_open + spacer )[0:lab_len]
#            self.gui.lbl_db_status.config(  text    =  lbl_text     )
#
#            lbl_text  = ( "Host: " + self.parameters.db_host    + spacer )[0:lab_len]
#            self.gui.lbl_db_host.config(    text    =  lbl_text     )
#
#            lbl_text  = ( "DB: " + self.parameters.db_db    + spacer )[0:lab_len]
#            self.gui.lbl_db_db.config(    text    =  lbl_text     )
#
#            lbl_text  = ( "User: " + self.parameters.db_user    + spacer )[0:lab_len]
#            self.gui.lbl_db_user.config(    text    =  lbl_text     )


    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        callback from gui button
        """
        from subprocess import Popen    # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, self.parameters.pylogging_fn ] )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + "parameters.py"

        from subprocess import Popen   # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ----------------------------------------------
    def os_open_parmxfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + self.parmeters_x + ".py"

        from subprocess import Popen, PIPE  # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ----------------------------------------------
    def os_open_helpfile( self,  ):
        """
        callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + "help.txt"

        from subprocess import Popen   # since infrequently used ??
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ------------------ callbacks for buttons -----------------

    def cb_graph( self,  ):
        """
        callback from gui button
        do the graph -- called from gui send to grapher
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
#        elif d_len == 1:
#            device = device_list[ 0 ]
#        else:
#            print( "multiple devices selected using the first one " )
#            device = device_list[0]

        self.grapher.do_graph( device_list, ts_begin, ts_end  )
    # ----------------------------------------------
    def cb_rb_select( self,  ):
        """
        call back for gui button
        """
        ix_rb     = self.gui.rb_var.get()
        print( "rb val", ix_rb )

        if    ix_rb == 0:
            self.db_select_from_parms()
        elif  ix_rb == 1:
            self.db_select_from_sun( 1 )
        elif  ix_rb == 2:
            self.db_select_from_sun( 2 )

        elif  ix_rb == 6:
            self.db_select_from_now( 1 )

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
        from tkinter import messagebox    # lazy import?
        db_file_name    = self.gui.get_db_file_name()
        if os.path.isfile( db_file_name ):
#            msg   =  f"File aexists: {db_file_name}"
#            AppGlobal.gui.display_info_string( msg )
#            print( f"file exists: {db_file_name}" )
            msg   =  f"Error: File ({db_file_name}) already exists."
            AppGlobal.gui.display_info_string( msg )
            messagebox.showinfo( "Error", msg )
            return
        msg     = f"Creating empty database in file ({db_file_name})."
        AppGlobal.gui.display_info_string( msg )
        define_db.create_db( db_file_name )

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
        AppGlobal.graphing.test_query()

# --------------------------------------

if __name__ == '__main__':
        """
        run the app
        """
        a_app = SmartPlugGraph(  )


# ====================== eof ========================



