# -*- coding: utf-8 -*-

"""
Purpose:
	for main programs in smart_plug.py and smart_plug_graph.py
	allows any module access to a set of application global values and functions
	typical use:
	from app_global import AppGlobal

	self.parameters    = AppGlobal.parameters

"""

import sys
import webbrowser
from   subprocess import Popen
from   pathlib import Path
import os
import psutil
from   tkinter import messagebox
import logging


# ----------------------------------------------

def addLoggingLevel( levelName, levelNum, methodName=None):
    """
    Comprehensively adds a new logging level to the `logging` module and the
    currently configured logging class.

     How to add a custom loglevel to Python's logging facility - Stack Overflow
     *>url  https://stackoverflow.com/questions/2183233/how-to-add-a-custom-loglevel-to-pythons-logging-facility

    `levelName` becomes an attribute of the `logging` module with the value
    `levelNum`. `methodName` becomes a convenience method for both `logging`
    itself and the class returned by `logging.getLoggerClass()` (usually just
    `logging.Logger`). If `methodName` is not specified, `levelName.lower()` is
    used.

    To avoid accidental clobberings of existing attributes, this method will
    raise an `AttributeError` if the level name is already an attribute of the
    `logging` module or if the method name is already present

    Example
    -------
    >>> addLoggingLevel('TRACE', logging.DEBUG - 5)
    >>> logging.getLogger(__name__).setLevel("TRACE")
    >>> logging.getLogger(__name__).trace('that worked')
    >>> logging.trace('so did this')
    >>> logging.TRACE
    5

    """

    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
       #raise AttributeError('{} already defined in logging module'.format(levelName))
       return   # assum already set up ok -- could cause error in comtaminated environment

    if hasattr(logging, methodName):
       raise AttributeError('{} already defined in logging module'.format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
       raise AttributeError('{} already defined in logger class'.format(methodName))

    # This method was inspired by the answers to Stack Overflow post
    # http://stackoverflow.com/q/2183233/2988730, especially
    # http://stackoverflow.com/a/13638084/2988730
    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, *args, **kwargs)
    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot )





class AppGlobal( object ):
    """
    use at class level ( do not _init_ ) for application globals, similar to but different from parameters
    some global functions
    """
    force_log_level         = 99        # value to force logging, high but not for errors

    # ----------- other important objects typically registered by their inits -- define as none to help document

    controller              = None      # populated by the controller
    parameters              = None      # populated by parameters
    gui                     = None      # populated by the gui
    logger                  = None      # populated by the controller
    graph_live              = None      # object for graphing
    helper                  = None      # populated externally by...
    #helper_thread_id        = None      # set by run in helper thread
    main_thread_id          = None
    logger_id               = None      # populated by the controller
    scheduled_event_list    = None      # populated externally by... -- think dead

    parameter_dicts         = {}        # set up in parameters ????? -- see and example std setup somw where
    smartplug_adapter_list  = None      # from controller.smartplug_adapter_list
    db_file_name            = None      # initially fetched from controller, later gui may update  this is a bad idea -- drop
    lock_db_file_name       = False     # just an idea, needs functions like check_lock_db_file_name  located where !!
    graph_live_flag         = False     # true for live graph
    graph_app               = False     # true if we are the db/graph version of the app
#    live_graph_opt          = 1         # 1 = all in helper                this is just an experiment


    # for the hours in the gui and their conversion to time
    dd_hours                = [ "0 Begin Day","01 - 1am","02 2am","03 3am","04 4am","05 5am","06 6am","07 7am","08 8am","09 9am","10 10am","11 11am","12 12am Noon",
                             "13 - 1pm","14 2pm","15 3pm","16 4pm","17 5pm","18 6pm","19 7pm","20 8pm","21 9pm","22 10pm","23 11pm",  ]


    # cls not yet defined
    # this gives the name notice to force_log_level... perhaps a better name might be used
    addLoggingLevel( "Notice", force_log_level, methodName=None)


    # ----------------------------------------------
    def __init__(self,  controller  ):

        y  = 1/0    # this guy should not be created and this stops it
        pass

    # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
		what it says
        see parameters for different types of files and nameing that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
#           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
#        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            ret = Popen( [ cls.parameters.ex_editor, str(a_join) ] )
#            print( f"help .txt {a_join} returned {a_join}")
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
#        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
#        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def show_process_memory( cls, call_msg = "", log_level = None, print_it = False ):
        """
        log and/or print memory usage
        """
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"{call_msg}process memory = {mem_mega:10,.2f} mega bytes "
        if print_it:
            print( msg )
        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )
        msg           =  f"{mem_mega:10,.2f} mega bytes "
        return ( mem, msg )

    # ----------------------------------------------
    @classmethod
    def log_if_wrong_thread( cls, id, msg = "forgot to include msg", main = True ):
        """
        debugging aid
        check if called by intended thread
        main thread must be set first
        ex:   AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )
        """
        on_main = ( id == cls.main_thread_id )

        if main:
            ok  = on_main
        else:
            ok = not( on_main )

        if not ok:
            msg    = f"In wrong thread = {cls.name_thread( id )}: + {msg}"
            cls.logger.log( cls.force_log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def name_thread( cls, id, ):
        """
        return thread name Main/Helper
        ex call:  AppGlobal.name_thread( threading.get_ident(),  )
        """
        if  cls.main_thread_id is None:
            y= 1/0   # cheap exception when main_thread not set up

        if id == cls.main_thread_id:
            ret = f"Main"
        else:
            ret = f"Helper"

        return ret

    # ----------------------------------------------
    @classmethod
    def thread_logger( cls, id, call_msg = "", log_level = None ):
        """
        debugging aid
        log a message, identifying which thread it came from
        ex call: AppGlobal.thread_logger( threading.get_ident(), "here we are", 50  )
        """
        thread_name   = cls.name_thread( id )
        msg  = f"in {thread_name} thread>> {call_msg}"

        if not ( log_level is None ):
            cls.logger.log( log_level,  msg )

    # ----------------------------------------------
    @classmethod
    def about( cls,   ):
        """
		show about box -- might be nice to make simple to go to url ( help button )
        """
        url   =  r"http://www.opencircuits.com/SmartPlug_Help_File"
        __, mem_msg   = cls.show_process_memory( )
        msg  = f"{cls.controller.app_name}  version:{cls.controller.version} \n  by Russ Hensel\n  Memory in use {mem_msg} \n  Check <Help> or \n     {url} \n     for more info."
        messagebox.showinfo( "About", msg )

    # ----------------------------------------------
    @classmethod
    def os_open_txt_file( cls, txt_file ):
        """
        open a text file with system configured editor
		?? could check for validity of the editor or use try except
        """
#        from subprocess import Popen
#        proc = Popen( [ cls.parameters.ex_editor, txt_file ] )


#        from subprocess import Popen, PIPE  # since infrequently used ??

        try:
            proc = Popen( [ cls.parameters.ex_editor, txt_file ] )

        except Exception as excpt:
             cls.logger.error( "os_open_logfile exception trying to use >" + str( cls.parameters.ex_editor ) + "< to open file >" + str( cls.parameters.pylogging_fn ) +
                              "< Exception " + str( excpt ) )
#             Add a message box hter as well as logger


     # ----------------- debuging ----------------
    def to_str():
        """
        debug aid, but dead
        convert some of AppGlobals contents to a string for debugging - left over from some other app
        might revive or delete
        """
        a_string   = (   "AppGlobal" +
                                  str (AppGlobal.parameter_dicts ) +
                           "\n    ---------- greenhouse ----------\n" + str( AppGlobal.parameter_dicts["greenhouse"]) )
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
    import smart_plug
    a_app = smart_plug.SmartPlug(  )


# ======================== eof ======================





