# -*- coding: utf-8 -*-

"""

for smart_plug

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

class AppGlobal( object ):
    """
    use at class level ( do not _init_ ) for application globals, similar to but different from parameters
    some global functions
    """
    force_log_level         = 99        # value to force logging, high but not for errors

    # ----------- other important objects registerd by their inits

    controller              = None      # populated by the controller
    parameters              = None      # populated by parameters
    gui                     = None      # populated by the gui
    logger                  = None      # populated by the controller
    graph_live              = None      # object for graphing
    helper                  = None

    logger_id               = None      # populated by the controller
    scheduled_event_list    = None

    parameter_dicts         = {}        # set up in parameters ????? -- see and example std setup somw where
    smartplug_adapter_list  = None      # from controller.smartplug_adapter_list
    db_file_name            = None     # initially fetched from controller, later gui may update  this is a bad idea -- drop
    lock_db_file_name       = False     # just an idea, needs functions like check_lock_db_file_name  located whree !!
    graph_live_flag         = False     # true for live graph
    graph_app               = False     # true if we are the db/graph version of the app

    # for the hours in the gui and their conversion to time
    dd_hours                = [ "0 Begin Day","01 - 1am","02 2am","03 3am","04 4am","05 5am","06 6am","07 7am","08 8am","09 9am","10 10am","11 11am","12 12am Noon",
                             "13 - 1pm","14 2pm","15 3pm","16 4pm","17 5pm","18 6pm","19 7pm","20 8pm","21 9pm","22 10pm","23 11pm",  ]

    def __init__(self,  controller  ):

        y  = 1/0    # this guy should not be created
        pass


    # ----------------------------------------------
    @classmethod
    def os_open_help_file( cls, help_file ):
        """
        see parameters for different types of files and nameing that will work with this
        """
        #help_file            = self.parameters.help_file
        if help_file.startswith( "http:" ) or help_file.startswith( "https:" ):
           ret  = webbrowser.open( help_file, new=0, autoraise=True )    # popopen might also work with a url
           print( f"help http: {help_file} returned {ret}")
           return

        a_join        = Path(Path( help_file ).parent.absolute() ).joinpath( Path( help_file ).name )
        print( f"a_join {type( a_join )} >>{a_join}<<" )

        #if a_join.endswith( ".txt" ):
        if a_join.suffix.endswith( ".txt" ):
            ret = Popen( [ cls.parameters.ex_editor, str(a_join) ] )
            print( f"help .txt {a_join} returned {a_join}")
            return

        file_exists   = os.path.exists( a_join )
        print( f"file {a_join} exists >>{file_exists}<<" )
        #full_path     = Path( help_file ).parent.absolute()
        print( f"a_join {a_join}" )
        help_file     = str( a_join )

        ret = os.popen( help_file )
        print( f"help popopen  {help_file} returned {ret}")

    # ----------------------------------------------
    @classmethod
    def show_process_memory( cls, call_msg = "", log_level = None ):
        """
        !! not really finished
        """

        # now most of setupe memory has been allocated -- may want to chekc in again later, save this value ??
        process      = psutil.Process(os.getpid())    #  import psutil
        mem          = process.memory_info().rss
        # convert to mega and format
        mem_mega     = mem/( 1e6 )
        msg          = f"{call_msg}process memory = {mem_mega:10,.2f} mega bytes "
        print( msg )
        if not ( log_level is None ):
            logger.log( log_level,  msg )
        msg           =  f"{mem_mega:10,.2f} mega bytes "
        return ( mem, msg )

    # ----------------------------------------------
    @classmethod
    def about( cls,   ):
        """

        """
        url   =  r"http://www.opencircuits.com/SmartPlug_Help_File"
        __, mem_msg   = cls.show_process_memory( )
        msg  = f"{cls.controller.app_name}  version:{cls.controller.version} \n  by Russ Hensel\n  Memory in use {mem_msg} \n  Check <Help> or \n     {url} \n     for more info."
        messagebox.showinfo( "About", msg )



    # ----------------------------------------------
    @classmethod
    def os_open_txt_file( cls, txt_file ):
        """
        see parameters for different types of files and nameing that will work with this
        """
        from subprocess import Popen
        proc = Popen( [ cls.parameters.ex_editor, txt_file ] )

     # ----------------- debuging ----------------
    def to_str():
        """
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





