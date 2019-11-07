# -*- coding: utf-8 -*-

"""
 this is the module that actually does the smart plug graphing from the database

    !! remember to zero out the data in the adapters

"""


#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
#import matplotlib.pyplot as plt
#import pylab

import matplotlib.pyplot as plt     # plotting stuff
import logging
#import time
import datetime
import sqlite3 as lite
import os

# --------- local imports
from   app_global import AppGlobal
# import parameters
import line_style

# ========================== Begin Class ================================
class Grapher:

    def __init__(self, ):
        #self.controller     = AppGlobal.controller
        self.parameters     = AppGlobal.parameters
        AppGlobal.graphing  = self

        #self.myLogger       = aController.myLogger
        self.logger         = logging.getLogger( AppGlobal.parameters.logger_id + ".sp_graph")
        self.logger.info( "in Grapher __init__" )
        self.line_style     = line_style.LineStyle()   # this gives differnt line styles to different graph lines

    # ---------------------------------------
    def do_graph( self, db_device_adapters, ts_begin, ts_end  ):
        """
        db_device_adapters   list of device_adapters

        fetch data from database print and do a simple graph
        this interfaces back to the controller, the rest do not
        indirect to make easer to mess about
        """
        self.end_graph()   # if an old one is hanging around
        self.db_device_adapters    = db_device_adapters

        self.graph_power_energy( ts_begin, ts_end, min_points = 10 )

#        # ------------- hide and restore root -- seems necessary in a terminal window
#        AppGlobal.gui.root.withdraw()
#        self.graph_power_energy( ts_begin, ts_end, min_points = 10 )
#        AppGlobal.gui.root.deiconify()

    # ---------------------------------------
    def end_graph( self,  ):
        """
        end graph even if none ( silent on error )
        """
        plt.close()

    # ---------------------------------------
    def graph_power_energy ( self,  db_start, db_end, min_points ):
        """
        still testing
        ( db_start, db_end  -> ) db_start and db_end are both tuples  -- used to be
        [ 0] date in string format     [1] a timestamp
        return nothing
        """
        db_file_name   = AppGlobal.gui.get_db_file_name()

        #  db_file_name    = AppGlobal.gui.bw_for_db.get_text()
        if not( os.path.isfile( db_file_name  )):
            msg     = f"db file does not exist: {db_file_name}"
            print( msg  )   # perhaps get rid of these or control thru parameters, or redirect to log
            AppGlobal.gui.display_info_string( msg, update_now = True )
            return

        self.line_style.reset()

        # prep data
        # if no data is found we need these
        self.graph_time_units  = self.parameters.graph_db_time_units
        self.graph_time_zero   = self.parameters.graph_db_time_zero

        for i_device_adapter in self.db_device_adapters:
#            db_select( self,  db_start, db_end, )

            #time_data, inst_pw_data, total_energy_data,    = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
            #i_device_adapter.retrived_data_cache  = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )  # just do it in _prep_data
            i_device_adapter.db_select(         db_start, db_end, )

        ok    = self.prep_time_convert( )
        if not ok:
            msg    = "No data so ... Graph done."
            AppGlobal.gui.display_info_string( msg )
            return

        for i_device_adapter in self.db_device_adapters:
            # power does not need adjustment
            i_device_adapter.adj_db_data_energy(                            )
            i_device_adapter.adj_db_data_time(   self.time_convert_function )

        # ------------ graph first axis
        fig, ax1     = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )
        color        = 'tab:red'

        ax1.set_title(  f"Power and Energy for Device SmartPlugs" );
        ax1.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}")   # these have been set multiple times

        ax1.set_ylabel(  "Power (Watts)", color=color )   # done in next line seems not to work
        ax1.grid( linestyle='-', linewidth='0.5', color='red' )

        ax1.set_ylim(  self.parameters.graph_inst_power_min, self.parameters.graph_inst_power_max )  # !! what is the auto

        for i_device_adapter in self.db_device_adapters:
            i_device_adapter.graph_power_from_db( line_style = self.line_style, ax = ax1  )

#        ax1.relim()
#        ax1.autoscale_view( True,True,True )

        ax1.tick_params( axis= 'y', labelcolor = color)

        ax1.legend( loc = 2 )

        # ------------ graph second axis power
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'

        ax2.set_ylabel( "Energy (watt * hr)", color = color)  # we already handled the x-label with ax1
        ax2.set_ylim(  self.parameters.graph_total_energy_min, self.parameters.graph_total_energy_max )  # perhaps just turn off, for auto scale

        for i_device_adapter in self.db_device_adapters:
            i_device_adapter.graph_energy_from_db( line_style = self.line_style, ax = ax2  )

        ax2.tick_params( axis='y', labelcolor = color )

        ax2.legend(['ax2 Total Energy legend'])
        ax2.legend( loc = 1 )

        # no error but does not seem to change anything
#        ax2.relim()
#        ax2.autoscale_view( True,True,True )

        # ----- finish up
        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) gives second plot empty
        # may need a way to flush or force a gui repaint
        msg    = "... Graph ready..."
        AppGlobal.gui.display_info_string( msg, update_now = True )

        # plt.draw() # trying to get autoscale working but no
        plt.show( block = False )   # try as experiment  -- seems ok also see withdraw in earlier call
        msg    = "... Graph done."
        AppGlobal.gui.display_info_string( msg )

    # ---------------------------------------
    def export_csv( self, db_start, db_end, min_points = 10, csv_file_name = "data.csv" ):
        """
        needs update !! will throw error  need to append data so will work for multiple devices ??  or make take a list of device adapters
        think is passed the name of the adapter should be a list of adapters like graph
        ?? file name check -- now fixed, and we append
        add sep to parameters ??
        add csv file to parameters
        ?? more title stuff
        """
        #x = 1/0   # this uses the data cache, to work we need to graph first ( prep data ??? ) to populate cache, then how about a clean up
        msg        = f"Export data to csv file {csv_file_name}..."
        AppGlobal.gui.display_info_string( msg )
        sep     = "\t"
        for i_device_adapter in self.db_device_adapters:
            #time_data, inst_pw_data, total_energy_data,    = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
            i_device_adapter.retrived_data_cache        = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
            time_data, inst_pw_data, total_energy_data,  = i_device_adapter.retrived_data_cache

            device_name       = i_device_adapter.name

            if time_data is None:
                msg        = f"No data for {device_name}."
                AppGlobal.gui.display_info_string( msg )
            else:
                with open( csv_file_name, "a" ) as a_file:  # we are appending
                    a_file.write( f'"device"{sep}"time_data"{sep}"inst_pw_data"{sep}"total_energy_data"\n' )
                    for ix_list, i_time in enumerate( time_data ):
                        a_file.write( f"{device_name}{sep}{time_data[ ix_list ]}{sep}{inst_pw_data[ ix_list ]}{sep}{total_energy_data[ ix_list ]}\n" )

        msg        = f"...CSV file complete."
        AppGlobal.gui.display_info_string( msg )

    # --------------------------------
    def prep_time_convert( self,  ):
        """
        return True if data else False
        """
        # may or may not be required
        min_time    = None
        max_time    = None
        got_data    = False

        for i_device_adapter in self.db_device_adapters:
            time_list    = i_device_adapter.gd_time
            if len( time_list ) > 0:
                if min_time is None:
                    min_time = time_list[ 0]   # relies on lists being sorted
                    max_time = time_list[-1]
                else:
                    min_time = min( min_time, time_list[ 0] ) # relies on lists being sorted
                    max_time = max( max_time, time_list[-1] )
                got_data = True

        if not got_data:
            print( "no data fix this " )
#            y = 1/0
            return False

        print( f"min max {min_time} {max_time} {got_data}" )
        zero          = AppGlobal.parameters.graph_db_time_zero.lower()
        print( f"time zero {zero}" )
        if   zero in [ "db_sql_begin",   ]:
            #convert_offset     =  time_data[0]      # sec to minutes
            convert_offset     =  db_start
            a_datetime          = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"sql select begin( {a_datetime} )"

        elif zero in  [ "data_begin" ]:
            convert_offset     = min_time
            a_datetime         = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"first data point( {a_datetime} )"

        else:  # default or error ??
            convert_offset     =  db_start
            a_datetime          = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"sql select begin( {a_datetime} )"

#        print( f"parameters say units {self.parameters.graph_time_units}"  )
        units  = AppGlobal.parameters.graph_db_time_units.lower()
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

        print( f"prep_time_convert convert_offset {convert_offset} convert_factor {convert_factor}")
        self.time_convert_function =  (lambda x: ( ( x - convert_offset ) * convert_factor ) )

        return True

        # do the convert here ???

#    # --------------------------------
#    def _prep_data( self, db_device_adapter,  db_start, db_end, min_points  ):
#        """
#        fetch from db and transform as per parameters
#        return data in a tuple each element a list
#        load some graph lables in instance variables for graph use  -- or move to return, perhaps named tuple
#        !! min points not implemented
#        !! allow multiple devices ??
#        """
#        db_device_adapter._db_select(          db_start, db_end, )
#        db_device_adapter._adj_db_data_time(   db_start, db_end, )
#        db_device_adapter._adj_db_data_energy(                    )



# --------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import   smart_plug_graph
        a_app = smart_plug_graph.SmartPlugGraph(  )


# ===================== eof ====================================



