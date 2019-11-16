# -*- coding: utf-8 -*-

"""
Purpose:
    part of smart_plug.SmartPlug
    use as central point in live graphing
    init graphing
    polling some code for begin same as end
"""


#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
#import matplotlib.pyplot as plt
#import pylab

import matplotlib.pyplot as plt     # plotting stuff
#import logging
import time
#import datetime
#import sqlite3 as lite
#import os
import threading

# --------- local imports
from   app_global import AppGlobal
#import parameters
import line_style

# ========================== Begin Class ================================
class GraphLive:

    def __init__(self, ):
        #self.controller      = AppGlobal.controller
        self.parameters       = AppGlobal.parameters
        AppGlobal.graph_live  = self

        self.line_style     = line_style.LineStyle()   # this gives different line styles to different graph lines

        self.debug_count    = 0

    # ----------------------------------------------
    def end_graph_live_evt( self, evt ):
        """
        basically strip off event and forward
        """
        print( f"end_graph_live_evt  {evt}")  # debug
        self.end_graph_live()

    # ----------------------------------------------
    def end_graph_live( self, ):
        """
        call from main thread
        end the live graphing
        """
        print( "end_graph_live" )
        AppGlobal.graph_live_flag         = False
        AppGlobal.graph_live_flag         = False
        ## off with the check box ... this is uggly
        AppGlobal.gui.graph_live_var.set( 0 )
        # self.graphing            = False

        for i_adapter in AppGlobal.smartplug_adapter_list:
            i_adapter.end_graph_live(   )   # this is a setup it does not start graphing by itself

        plt.close()

    # ---------------------------------------
    def start_graph_live( self, ):
        """
        call from main thread
        start off a session of live graphing -- need to run in main thread
        moved from the plug
        no validation if start is ok
        no inactivation of controls .... even this should perhaps come from a checkbox


        what do we want to do:
            graph only plugs that are being monitored or recorded
            accumulate the data in a list ( list of tuples might be better than two lists or even a numpy type thing )

            ??? what is monitor, record is turned off ( keep data and graph line so far stop adding to data )
            ??? what if new adapter is turned on ( was it on earlire ?? )
            ??? export csv    export all cached data to a csv, if none just a message
        """
        msg    =  "GraphLive.start_graph_live"
#        AppGlobal.what_thread( threading.get_ident(), msg, 20  )
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

        self.rescale_time_function        = lambda x: x     # default identity function
        self.set_rescale_time_function()

        #Set up plot
        self.figure, self.ax   = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )

        self.figure.canvas.mpl_connect( 'close_event', self.end_graph_live_evt )

        plt.legend( loc=2 )    # for label to show up ?  # made small sq show up no content, too early ?
        # lets try to build the line in each adapter
        self.lines,            = self.ax.plot([],[], 'o', color="red", linewidth=2.5, linestyle="-"  )     # the line is the thing to update ... can we add later, lets assume we can
        #Auto scale on unknown axis and known limits on the other
        self.ax.set_autoscaley_on( True )
        #self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid( linestyle='-', linewidth='0.5', color= 'red' )
        self.ax.tick_params( axis= 'y', labelcolor= 'red' )

        self.ax.set_title(  f"Power measured by SmartPlugs" );
        self.ax.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}" )   # these have been set multiple times
        self.ax.set_ylabel( f"Power in watts" )   # these have been set multiple times

        for i_adapter in AppGlobal.smartplug_adapter_list:
            i_adapter.start_graph_live( self.ax  )   # this is a setup it does not start graphing by itself
        plt.show( block = False )
        AppGlobal.logger.error( "GraphLive.start_graph_live complete" )
        AppGlobal.graph_live_flag      = True        # this will kick off in polling set last

        # call polling right away or just do redraw ??

    # ---------------------------------------
    def polling_mt( self, ):
        """
        polling for the main thread ( gui thread )
        """
        msg = "GraphLive.polling_mt  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )
#        AppGlobal.logger.error( msg )

        # collect flags from the individual devices
        need_redraw_flag = False
        for i_adapter in AppGlobal.smartplug_adapter_list:
            if i_adapter.update_graph_live(  ):
                need_redraw_flag = True

        #AppGlobal.logger.error( "GraphLive.polling_mt test next" )
        if need_redraw_flag:
            AppGlobal.logger.error( "GraphLive.polling_mt need redraw True" )
            self.ax.relim()
            self.ax.autoscale_view()
                #We need to draw *and* flush
            AppGlobal.logger.error( "GraphLive.polling_mt next draw flush" )
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
            plt.legend( loc=2 )                 # help with update  -- seems to work
#            AppGlobal.logger.error( "GraphLive.polling_mt polling show next" )
            plt.show( block = False )
#            AppGlobal.logger.error( "GraphLive.polling_mtpolling post next" )

            # ------------ for tracking memory use
            self.debug_count += 1
            if self.debug_count > 50:
                AppGlobal.show_process_memory( "GraphLive.polling_mt polling time to log", log_level = 20 )
                self.debug_count = 0

    # ---------------------------------------
    def polling_ht( self, ):
        """
        polling for the helper thread
        not sure this is ever needed
        """
        msg = "GraphLive.polling_ht  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = False  )
        #print( "GraphLive.polling_ht running...")

    # ---------------------------------------
    def polling( self, ):
        """
        dead make sure delete
        adjust how often this is updated  -- as here needs to run in main thread, may need two, one for main one for
        may need to be called in main thread not helper ?? works in ipython  spyder, but not in shell
        """
        y = 1/x
#        print( f" GraphLive polling " )

    # ---------------------------------------
    def set_rescale_time_function( self,  ):
        """
        setup the function for rescaling time
        see similar in graph_from_db
        self.rescale_time        = lambda x: x     # default identity function
        set_rescale_function()

        self.graph_live_time_units   = "min"  # ?? "hour" "min" days seconds.... add more   #  day hour  use my converter in future
        self.graph_db_time_zero      = "now"    #   time labeled as 0 on the graph
        self.graph_db_time_zero      = "now"    #   time labeled as 0 on the graph
        #self.graph_db_time_zero      = "begin_toeay"    #   time labeled as 0 on the graph
        self.graph_live_time_units   = "min"  # ?? "hour" "min" days seconds.... add more   #  day hour  use my converter in future
        self.graph_live_time_zero      = "now"
        """
        zero          = self.parameters.graph_live_time_zero.lower()
        if   zero in [ "now",   ]:
            convert_offset     =  time.time()
            self.graph_time_zero   = "start of graphing"
        elif zero in  [ "begin_today", ]:
            time_struct        = time.localtime( ts )
            convert_offset      = time.mktime( (  time_struct[0], time_struct[1], time_struct[2], 0, 0, 0, 0, 0, 0  ) )
            self.graph_time_zero   = "start of today"
        else:  # default or error ??
            convert_offset     =  0

#        print( f"parameters say units {self.parameters.graph_time_units}"  )
        units  = self.parameters.graph_live_time_units.lower()
        if  units in [ "min", "minutes" ]:
            convert_factor     =  1./60.      # sec to minutes
            self.graph_time_units = "minutes"

        elif units in  [ "hr", "hour", "hours" ]:
            convert_factor     =  1./( 60. * 60 )
            self.graph_time_units = "hours"

        elif units in [ "day", "days",  ]:
            convert_factor     =  1./( 60. * 60 * 24 )
            self.graph_time_units = "days"

        else: # seconds
            convert_factor         =  1.
            self.graph_time_units  = "seconds"

        self.rescale_time_function  =  lambda x: ( ( x - convert_offset ) * convert_factor )  # conversion on timestamps

    # ---------------------------------------
    def export_csv( self,  csv_file_name = "live_data.csv" ):
    #def export_csv( self, db_device_adapters,  db_start, db_end, min_points = 10, csv_file_name = "live_data.csv" ):
        """
        needs update !! will throw error  need to append data so will work for multiple devices ??  or make take a list of device adapters
        think is passed the name of the adapter should be a list of adapters like graph
        ?? file name check -- now fixed, and we append
        add sep to parameters ??
        add csv file to parameters
        ?? more title stuff
        """
#        msg  = "May be implemented at some point."
#        messagebox.showinfo( "Not Yet Implemented", msg )
        #x = 1/0   # this uses the data cache, to work we need to graph first ( prep data ??? ) to populate cache, then how about a clean up
        msg        = f"Export data to csv file {csv_file_name}..."
        AppGlobal.gui.print_info_string( msg )

        sep        = "\t"    # seperator for values \t is tab
        for i_device_adapter in  AppGlobal.smartplug_adapter_list:
            times           = i_device_adapter.gd_time
            powers          = i_device_adapter.gd_power
            #energies        = i_device_adapter.gd_energy    # no energy for graph live ??
            device_name     = i_device_adapter.name

            if len( times ) == 0:
                msg        = f"No data for {device_name}."
                AppGlobal.gui.print_info_string( msg )
            else:
                with open( csv_file_name, "a" ) as a_file:  # a  we are appending
                    a_file.write( f'"device"{sep}"time_data"{sep}"inst_pw_data"{sep}"energy_data"\n' )
                    for ix_list, i_time in enumerate( times ):
                        #a_file.write( f"{device_name}{sep}{times[ ix_list ]}{sep}{powers[ ix_list ]}{sep}{energies[ ix_list ]}\n" )
                        a_file.write( f"{device_name}{sep}{times[ ix_list ]}{sep}{powers[ ix_list ]}\n" )
                    msg        = f"...{device_name}  {ix_list} lines..."
                    AppGlobal.gui.print_info_string( msg )
        msg        = f"...{csv_file_name} file complete."
        AppGlobal.gui.print_info_string( msg )

# --------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import smart_plug
        a_app = smart_plug.SmartPlug(  )

# ===================== eof ====================================






