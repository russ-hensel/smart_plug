# -*- coding: utf-8 -*-

"""
Purpose:
    use as central point in live graphing
    init graphing
    polling some code for begin same as end
"""


#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
#import matplotlib.pyplot as plt
#import pylab

import matplotlib.pyplot as plt     # plotting stuff
import logging
import time
import datetime
import sqlite3 as lite
import os

# --------- local imports
from   app_global import AppGlobal
import parameters
import line_style

# ========================== Begin Class ================================
class GraphLive:

    def __init__(self, ):
        #self.controller      = AppGlobal.controller
        self.parameters       = AppGlobal.parameters
        AppGlobal.graph_live  = self

        self.line_style     = line_style.LineStyle()   # this gives differnt line styles to different graph lines

    # ---------------------------------------
    def start_graph_live( self, ):
        """
        start off a session of live graphing
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
        self.rescale_time_function        = lambda x: x     # default identity function
        self.set_rescale_time_function()

        #Set up plot
        self.figure, self.ax   = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )

        # lets try to build the line in each adapter
        self.lines,            = self.ax.plot([],[], 'o', color="red", linewidth=2.5, linestyle="-"  )     # the line is the thing to update ... can we add later, lets assume we can
        #Auto scale on unknown axis and known limits on the other
        self.ax.set_autoscaley_on(True)
        #self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid( linestyle='-', linewidth='0.5', color= 'red' )
        self.ax.tick_params( axis= 'y', labelcolor= 'red' )

        self.ax.set_title(  f"Power measured by SmartPlugs" );
        self.ax.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}" )   # these have been set multiple times

        for i_adapter in AppGlobal.smartplug_adapter_list:
            i_adapter.start_graph_live( self.ax  )   # this is a setup it does not start graphing by itself

        AppGlobal.graph_live_flag      = True      # this will kick off in polling set last

        # call polling right away or just do redraw ??

    # ---------------------------------------
    def polling( self, ):
        """
        adjust how often this is updated
        """
#        print( f" GraphLive polling " )

        need_redraw_flag = False
        for i_adapter in AppGlobal.smartplug_adapter_list:
            if i_adapter.update_graph_live(  ):
                need_redraw_flag = True

        if need_redraw_flag:
            self.ax.relim()
            self.ax.autoscale_view()
                #We need to draw *and* flush
            self.figure.canvas.draw()
            self.figure.canvas.flush_events()

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

#    # ---------------------------------------
#    def export_csv( self, db_device_adapters,  db_start, db_end, min_points = 10, csv_file_name = "data.csv" ):
#        """
#        needs update !! will throw error  need to append data so will work for multiple devices ??  or make take a list of device adapters
#        think is passed the name of the adapter should be a list of adapters like graph
#        ?? file name check -- now fixed, and we append
#        add sep to parameters ??
#        add csv file to parameters
#        ?? more title stuff
#        """
#        #x = 1/0   # this uses the data cache, to work we need to graph first ( prep data ??? ) to populate cache, then how about a clean up
#        msg        = f"Export data to csv file {csv_file_name}..."
#        AppGlobal.gui.display_info_string( msg )
#        sep     = "\t"
#        for i_device_adapter in db_device_adapters:
#            #time_data, inst_pw_data, total_power_data,    = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
#            i_device_adapter.retrived_data_cache        = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
#            time_data, inst_pw_data, total_power_data,  = i_device_adapter.retrived_data_cache
#
#            device_name       = i_device_adapter.name
#
#            if time_data is None:
#                msg        = f"No data for {device_name}."
#                AppGlobal.gui.display_info_string( msg )
#            else:
#                with open( csv_file_name, "a" ) as a_file:  # we are appending
#                    a_file.write( f'"device"{sep}"time_data"{sep}"inst_pw_data"{sep}"total_power_data"\n' )
#                    for ix_list, i_time in enumerate( time_data ):
#                        a_file.write( f"{device_name}{sep}{time_data[ ix_list ]}{sep}{inst_pw_data[ ix_list ]}{sep}{total_power_data[ ix_list ]}\n" )
#
#        msg        = f"...CSV file complete."
#        AppGlobal.gui.display_info_string( msg )



# --------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import smart_plug
        a_app = smart_plug.SmartPlug(  )

# ===================== eof ====================================






