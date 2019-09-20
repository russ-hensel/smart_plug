#!python3
# -*- coding: utf-8 -*-


"""
Purpose:
    smart_plug.py  ( tp link ) app with a gui
    this is the main program, start it
    related program smart_plug_graph.py

Environment:

        Spyder 3.3.6
        Python 3.6
        Tkinker
        .....
        tested in Win 10 should work in all os's

See Also:
        smart_plug_help.txt
        readme.txt
        readme_rsh.txt


"""

import logging
import sys
import os
import time
import datetime
import traceback
import queue
#import threading
import importlib
import pyHS100

# ----------- local imports --------------------------
import parameters
import gui
from   app_global import AppGlobal
import smart_plug_helper
import smart_plug_adapter


# ========================== Begin Class ================================
class SmartPlug( object ):
    """
    main and controller class for the application
    """
    def __init__(self ):
        """
        mostl instances declared here or in restart
        """
        # ------------------- basic setup --------------------------------
        print( "" )
        print( "=============== starting SmartPlug ========================= " )
        print( "" )
        print( "     -----> prints may be sent to log file !" )
        print( "" )

        AppGlobal.controller        = self
        self.app_name               = "SmartPlug"
        self.version                = "Ver5 2019 09 19.0"

        self.gui                    =  None  # the gui created later
        self.no_restarts            =  -1    # counter for the number of times the application is restarted

        # ----------- for second thread -------
        self.queue_to_gui           = None
        self.queue_from_gui         = None
#        self.gui_recieve_lock       = threading.Lock()   # when locked the gui will process recieve, aquired released in helper
                                                         # how different from just a variable set?
        self.restart( )

    # --------------------------------------------------------
    def restart(self ):
        """
        use to restart the app without ending it - also exten init
        parameters will be reloaded and the gui rebuilt
        args: zip
        ret: zip ... all sided effects
        """
        print( "===================restart===========================" )
        #global print
        self.no_restarts    += 1
        if self.gui is not None:

            self.logger.info( self.app_name + ": restart" )

            # need to shut down other thread
            self.post_to_queue( "stop", None  , (  ) )
            self.helper_thread.join()

            self.gui.close()
            try:
                importlib.reload( parameters )    # should work on python 3 but sometimes if not
            except Exception as ex_arg:
                reload( parameters )              # this is python 2

        self._polling_fail         = False   # flag set if _polling in gui thread fails

        self.is_first_gui_loop    = True
        self.ext_processing       = None     # built later frompermaters if specified
        self.logger               = None    # set later none value protects against call against nothing

        # ----- parameters

        self.parmeters_x          = "none"        # name without .py for parameters extension may ?? be replaced by command line args
        #self.__get_args__( )
        # command line might look like this
        # python smart_terminal.py    parameters=gh_paramaters

        self.parameters         = parameters.Parameters( )  #  std name -- open early may effect other
        self.starting_dir       = os.getcwd()    #

        self.smartplug_adapter_list     = []

        for i_device in self.parameters.device_list:
            i_smartplug_adapter                = smart_plug_adapter.SmartPlugAdapter()
            self.smartplug_adapter_list.append( i_smartplug_adapter  )
            i_smartplug_adapter.name           = i_device[ "name" ]
            i_smartplug_adapter.tcpip          = i_device[ "tcpip" ]
            AppGlobal.smartplug_adapter_list   = self.smartplug_adapter_list

        # get parm extensions  !! will this work on a reload ??
        if self.parmeters_x != "none":
            self.parmeters_xx   =  self.create_class_from_strings( self.parmeters_x, "ParmetersXx" )
            self.parmeters_xx.modify( self.parameters )

        self.logger_id          = self.parameters.logger_id       # std name
        self.logger             = self.config_logger()            # std name

        AppGlobal.logger        = self.logger
        AppGlobal.logger_id     = self.logger_id

        self.prog_info()

        # set up queues befor creating helper thread
        self.queue_to_helper    = queue.Queue( self.parameters.queue_length )   # send strings back to tkinker mainloop here
        self.queue_fr_helper    = queue.Queue( self.parameters.queue_length )
        self.helper_thread      = smart_plug_helper.HelperThread( )
        AppGlobal.helper        = self.helper_thread

        self.helper_thread.start()

#        AppGlobal.print_me()        # debug, take out
#        print( "==============================================" )

        self.gui                = gui.GUI(  )
        self.gui.root.after( self.parameters.gt_delta_t, self._polling )
        self.gui.run()

        self.post_to_queue( "stop", None  , (  ) )

        self.helper_thread.join()
        self.logger.info( self.app_name + ": all done" )

    # --------------------------------------------------------
    def config_logger( self, ):
        """
        configure the logger in usual way using the current parameters

        args: zip
        ret:  the logger
        """
        logger = logging.getLogger( self.logger_id  )

        logger.handlers = []
        logger.setLevel( self.parameters.logging_level )     # DEBUG , INFO	WARNING	ERROR	CRITICAL

        fh = logging.FileHandler(   self.parameters.pylogging_fn )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.info( "Done config_logger" ) #  .debug   .info    .warn    .error

        return logger

 # -------------------------------------------------------
    def prog_info( self ):
        """
        log info about program and its argument/enviroment to the logger
        after logger is set up
        args: zip
        ret:  zip
        log_msg = "a message "
        # debug info warning, error critical

        """
        fll         = AppGlobal.force_log_level
        logger      = self.logger

        if ( self.no_restarts == 0 ) :
            logger.log( fll,      "" )
            logger.log( fll,  "" )
            logger.log( fll,  "============================" )
            logger.log( fll,      "" )

            logger.log( fll, "Running " + self.app_name + " version = " + self.version ) # + " mode = " + parameters.mode )
            logger.log( fll,  "" )

        else:
            logger.log( fll,     "======" )
            logger.log( fll, "Restarting " + self.app_name + " version = " + self.version ) #+ " mode = " + parameters.mode )
            logger.log( fll,      "=====" )

        if len( sys.argv ) == 0:
            logger.log( fll, "no command line arg " )
        else:
            ix_arg = 0
            for aArg in  sys.argv:

                logger.log( fll, "command line arg " + str( ix_arg ) + " = " + sys.argv[ix_arg])
                ix_arg += 1

        logger.log( fll,  "current directory " +  os.getcwd() )
        logger.log( fll,  "COMPUTERNAME "      +  str( os.getenv( "COMPUTERNAME" ) ) )  # may not exist in linux

        start_ts     = time.time()
        dt_obj       = datetime.datetime.utcfromtimestamp( start_ts )
        string_rep   = dt_obj.strftime('%Y-%m-%d %H:%M:%S')
        logger.log( fll, "Time now: " + string_rep )

        return

    # --------------------------------------------------
    def post_to_queue( self, action, function, args ):
        """
        self.post_to_queue( action, function, args )
        request action by other thread
        """
        loop_flag          = True
        ix_queue_max       = 10
        ix_queue           = 0
        while loop_flag:
            loop_flag      = False
            ix_queue  += 1
            try:
                #print( "try posting " )
                self.queue_to_helper.put_nowait( ( action, function, args ) )
            except queue.Full:

                # try again but give _polling a chance to catch up
                print( "smart_terminal queue full looping" )
                self.logger.error( "queue to helper full looping" )
                # protect against infinit loop if queue is not emptied
                if self.ix_queue > ix_queue_max:
                    print( "too much queue looping" )
                    self.logger.error( "too much queue looping" )
                    pass
                else:
                    loop_flag = True
                    time.sleep( self.parameters.queue_sleep )

     # -------------------------------------------------------
    def _polling( self, ):
        """
        this is a private method
        _polling task runs continually in the GUI
        reciving data is an important task. but is it in this thread  any more  ??
        there is still some effectively dead stuff from the smart_terminal
        also auto tasks will be run from here
        _polling frequency set via taskDelta, ultimately in parameters
        http://matteolandi.blogspot.com/2012/06/threading-with-tkinter-done-properly.html
        safely invoke the method tk.after_idle to actually schedule the update. That's it!
        """
        """
        queue protocol, data = ( action, function, function_args )
        action            = a string
        function          = a function
        function_args     = arguments to function which will be called  function( function_args ) This should be a tuple
        """
        if self.is_first_gui_loop:
            # if we need a first loop item make a _polling_init that is called ??
            # should be moved to gui !! turn back on unless messing up whole app
            # print("lifting...")
#            self.gui.root.attributes("-topmost", True)  # seems to work
#            self.gui.root.lift()                        # did not work
            self.is_first_gui_loop    = False
#            self.gui.root.attributes("-topmost", False)  # seems to work
        try:   # this is for talking with the second thread
            ( action, function, function_args ) = self.rec_from_queue()
            while action != "":
                if action == "call":
                    #print( "controller making call" )
                    sys.stdout.flush()
                    function( *function_args )
                elif action == "rec":
                    self.gui.print_rec_string(  function_args[ 0 ] )
                elif action == "send":
                    # but where is it actually sent ??
                    self.gui.print_send_string( function_args[ 0 ] )
                elif action == "info":
                    self.gui.print_info_string( function_args[ 0 ] )

                ( action, function, function_args ) = self.rec_from_queue()

        except Exception as ex_arg:
            self.logger.error( "_polling Exception in smart_terminal: " + str( ex_arg ) )
            # ?? need to look at which we catch maybe just rsh
            (atype, avalue, atraceback)   = sys.exc_info()
            a_join  = "".join( traceback.format_list ( traceback.extract_tb( atraceback ) ) )
            self.logger.error( a_join )

        finally:
            if  self._polling_fail:
                pass
            else:
                #print 'In finally block for cleanup'
                self.gui.root.after( self.parameters.gt_delta_t, self._polling )  # reschedule event

        return

    # --------------------------------------------------
    def rec_from_queue( self, ):
        """
        take an item off the queue, think here for expansion may not be currently used.
        ( action, function, function_args ) = self.rec_from_queue()
        """
        try:
            action, function, function_args   = self.queue_fr_helper.get_nowait()
        except queue.Empty:
            action          = ""
            function        = None
            function_args   = None

        return ( action, function, function_args )

    # ----------------------------------------------
    def os_open_parmfile( self,  ):
        """
        used as callback from gui button
        """
        a_filename = self.starting_dir  + os.path.sep + "parameters.py"

        from subprocess import Popen, PIPE  # since infrequently used
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ----------------------------------------------
    def os_open_logfile( self,  ):
        """
        used as/by callback from gui button.  Can be called form gt
        """
        from subprocess import Popen, PIPE  # since infrequently used
        proc = Popen( [ self.parameters.ex_editor, self.parameters.pylogging_fn ] )

    # ----------------------------------------------
    def os_open_helpfile( self,  ):
        """
        used as callback from gui button
        """
#        a_filename = self.starting_dir  + os.path.sep + "parameters.py"
        a_filename = self.parameters.help_file
        from subprocess import Popen, PIPE  # since infrequently used
        proc = Popen( [ self.parameters.ex_editor, a_filename ] )

    # ------------------------------------------
    def cb_device_action( self, button_ix, action  ):
        """
        process devices perhaps on, off timer , see lambda setup in button creation
        mabe decode string in adapter as well
        """
#        print( f"controller.cb_device_action {button_ix}, {action}" )

#       check for valid index -- may be overly defensive, but so what
        if button_ix < len( AppGlobal.device_list ):
            i_device    = AppGlobal.smartplug_adapter_list[ button_ix ]
            tcpip       = i_device.tcpip
            plug        = pyHS100.SmartPlug( tcpip )
        else:
            msg      = f"invalid device index{button_ix}"
            self.gui.print_info_string( msg )
            self.logger.info( msg )
            return

        # test getting time
#        gui_combo      = i_device.gui_tk_combo
#        combo_contents = gui_combo.get()
#        print(f"combo_contents: {combo_contents}, {type(combo_contents)}")

        # wrap actions in try except and capture error info
        if   action == "info":
            # move code to device adapter
            #self.gui.print_info_string( tcpip )
            info    = plug.hw_info   # need to process this into something nice -- is this subset of get_sysinfo()
            #print( type( info ) )
            self.gui.print_info_string( str( info ) )
            # add more info
            info        = plug.get_sysinfo()
            info        = dict_to_str( info )
            self.gui.print_info_string( info )
#            label       = i_device.gui_tk_label
#            label.config( text = 'see info below' )
            msg  = "see info below"
            self.gui.display_device_label( self, msg, i_device  )

        elif action == "start":   # may make synomonus with on ??
            i_device.start_timer()

        elif action == "on":
            # ?? move messaging to i_device ??/
            i_device.on()

        elif action == "off":
            i_device.off()
#            msg     = f"Plug is_on: {plug.is_on }"
#            self.gui.print_info_string( msg )

        elif action == "record_on":
            i_device.record_on()
#            msg      = f"Record on plug is on : {plug.is_on }"
#            self.gui.print_info_string( msg )

        elif action == "record_off":
            i_device.record_off()
#            msg     = f"Record off plug is on : {plug.is_on }"
#            self.gui.print_info_string( msg )

        else:
            msg      = f"invalid action {action}"
            self.gui.print_info_string( msg )

   # ----------------------------------------------
    def cb_gui_test_1( self,  ):
        """
        call back for gui button
        """
        print( "cb_gui_test_1" )

#        # -----------------------
#        import db
#        a_db    = db.DBAccess()
#        ok      = a_db.open()
#        print( "db.open ", ok  )
#
#        a_db.close()

        #----------------------
        ret = AppGlobal.scheduled_event_list.test_query()
        print( ret )
        #self.helper_thread.toggle_lock()

# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    a_app = SmartPlug(  )






