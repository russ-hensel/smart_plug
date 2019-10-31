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
#        self.graph_4( db_device_adapter, ts_begin, ts_end, min_points = 10 )
#        self.graph_many( db_device_adapters[0], ts_begin, ts_end, min_points = 10 )
        self.graph_many_really( db_device_adapters, ts_begin, ts_end, min_points = 10 )

    # ---------------------------------------
    def end_graph( self,  ):
        """
        end graph even if none ( silent on error )
        """
        plt.close()

    # ---------------------------------------
    def graph_many_really ( self, db_device_adapters,  db_start, db_end, min_points ):
        """
        still testing
        ( db_start, db_end  -> ) db_start and db_end are both tuples  -- used to be
        [ 0] date in string forma     [1] a timestamp
        """
        db_file_name   = AppGlobal.gui.get_db_file_name()

        #db_file_name    = AppGlobal.gui.bw_for_db.get_text()
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

        for i_device_adapter in db_device_adapters:
                #time_data, inst_pw_data, total_energy_data,    = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )
                i_device_adapter.retrived_data_cache  = self._prep_data( i_device_adapter,  db_start, db_end, min_points  )

#                min_time_data     = time_data[0]
#                max_time_data     = time_data[-1]
#                device_name       = db_device_adapter.name
                # because of Nones, firguring this out is a mess leave for later
#                data              =  i_device_adapter.retrived_data_cache[ 0 ][0]
#                 if min_time_data = None:
#                     min_time_data =

        # ------------------- now plot new ------
        # may be that this is way of multiple plots on one canvas -- but here works for one plot
        #how to set figure size ?/

        #plt.figure( plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) )) ) us this get two graphs

        fig, ax1     = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )
        color        = 'tab:red'

        ax1.set_title(  f"Power and Energy for Device SmartPlugs" );
        ax1.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}")   # these have been set multiple times

        ax1.set_ylabel(  "Power (Watts)", color=color )   # done in next line seems not to work
        ax1.grid( linestyle='-', linewidth='0.5', color='red' )

        for i_device_adapter in db_device_adapters:
            self.line_style.get_next_style()
            time_data, inst_pw_data, total_energy_data,  = i_device_adapter.retrived_data_cache
            if  ( ( time_data is None ) or  len( time_data ) == 0  ):
                print( f"no data for {i_device_adapter.name}" )
                continue
            ax1.plot( time_data, inst_pw_data,          linestyle = self.line_style.linestyle,
                                                        marker    = self.line_style.markerstyle,
                                                        color     = self.line_style.colorstyle,
                                                        label     = i_device_adapter.name ) # label= "Power (Watts)" )

        ax1.tick_params( axis= 'y', labelcolor=color)

            #ax1.set_ylim( self.parameters.graph_inst_power_min, self.parameters.graph_inst_power_max )

#        inst_pw_data = [ ( x/2 ) for x in inst_pw_data ]
#        ax1.plot( time_data, inst_pw_data,         linestyle='--', marker='.', color='green', label = "label2" ) # label= "Power (Watts)" )

#        ax1.legend(['Power'])   # having trouble with this
#        ax1.legend( loc = 2 )  # what mean location

        ax1.legend( loc = 2 )

        # ------ second graph energy

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'

        ax2.set_ylabel( "Energy (watt * hr)", color=color)  # we already handled the x-label with ax1
        ax2.set_ylim(  self.parameters.graph_total_energy_min, self.parameters.graph_total_energy_max )

        for i_device_adapter in db_device_adapters:
            self.line_style.get_next_style()
            time_data, inst_pw_data, total_energy_data,  = i_device_adapter.retrived_data_cache
            if  ( ( time_data is None ) or  len( time_data ) == 0  ):
                print( f"no data for {i_device_adapter.name}" )
                continue
            ax2.plot( time_data, total_energy_data,     linestyle = self.line_style.linestyle,
                                                        marker    = self.line_style.markerstyle,
                                                        color     = self.line_style.colorstyle,
                                                        label     = i_device_adapter.name    )   # "Energy (Watts*hr)")  # label= "Power (Watts)" )

        ax2.tick_params( axis='y', labelcolor = color )

        ax2.legend(['ax2 Total Energy legend'])
        ax2.legend( loc = 1 )

        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) gives second plot empty
        # may need a way to flush or force a gui repaint
        msg    = "... Graph ready..."
        AppGlobal.gui.display_info_string( msg, update_now = True )
        plt.show()
        msg    = "... Graph done."
        AppGlobal.gui.display_info_string( msg )

    # ---------------------------------------
    def export_csv( self, db_device_adapters,  db_start, db_end, min_points = 10, csv_file_name = "data.csv" ):
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
        for i_device_adapter in db_device_adapters:
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
    def _prep_data( self, db_device_adapter,  db_start, db_end, min_points  ):
        """
        fetch from db and transform as per parameters
        return data in a tuple each element a list
        load some graph lables in instance variables for graph use  -- or move to return, perhaps named tuple
        !! min points not implemented
        !! allow multiple devices ??
        """
        msg   = f"Preparing data for {db_device_adapter.name}"
        AppGlobal.gui.display_info_string( msg )
        #self.logger.debug( f"_prep_data {db_start}, {db_end}" )

#        set_zero           = self.parameters.graph_time_zero  #      "max"   # min max
#        units              = self.parameters.graph_time_units     # "hour"   #  day hour  use my converter in future

        db_device_name           = db_device_adapter.name
        time_data                = []      # raw data on time may be timestamp......

        inst_pw_data             = []      #
        total_energy_data        = []      #

#         ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy )

        sql         = ( "SELECT plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy " +
                      " FROM plug_measurements   WHERE ( plug_time > ? ) AND ( plug_time < ? ) AND ( plug_name = ? ) order by plug_time asc" )

        a_datetime_begin     = datetime.datetime.fromtimestamp( db_start )
#        print( f"a_datetime_begin = { type(a_datetime_begin)}  {a_datetime_begin} " )

        a_datetime_end     = datetime.datetime.fromtimestamp( db_end )
#        print( f"a_datetime_end = { type(a_datetime_end)}  {a_datetime_end} " )

        db_file_name       = AppGlobal.gui.get_db_file_name()
#        db_file_name       = AppGlobal.db_file_name
        if not( os.path.isfile( db_file_name  )):
            msg   =  f"Error: db file does not exist: {db_file_name}"
            AppGlobal.gui.display_info_string( msg )
            return( None, None, None )

        sql_con = lite.connect( db_file_name )
        with sql_con:
            cur = sql_con.cursor()
#            print(f"db_device_name{db_device_name}")
            cur.execute( sql , ( db_start, db_end, db_device_name ) )

            # get rows one at a time in loop
            while True:
               row   = cur.fetchone()

               if row is None:
                   break
               print( f"{row}   [1] {row[1]}   {row[6]}" )

               time_data.append(           row[1] )
               inst_pw_data.append(        row[6] )
               total_energy_data.append(   row[7] )

        msg   =   f"For device {db_device_name}: data points fetched: {len( time_data )}"
        AppGlobal.gui.display_info_string( msg, update_now = True )

        if  len( time_data ) < 10:
            msg   =   f"Not enough data to process for {db_device_name}"
            AppGlobal.gui.display_info_string( msg )
            return( None, None, None )

        temp          = []     # temporary to build new time data will put back  ... !! list comp makes this not needed

        zero          = self.parameters.graph_db_time_zero.lower()
        if   zero in [ "db_sql_begin",   ]:
            #convert_offset     =  time_data[0]      # sec to minutes
            convert_offset     =  db_start
            a_datetime          = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"sql select begin( {a_datetime} )"

        elif zero in  [ "data_begin" ]:
            convert_offset     =  time_data[0]
            a_datetime         = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"first data point( {a_datetime} )"

        else:  # default or error ??
            convert_offset     =  db_start
            a_datetime          = datetime.datetime.fromtimestamp( convert_offset )
            self.graph_time_zero = f"sql select begin( {a_datetime} )"

#        print( f"parameters say units {self.parameters.graph_time_units}"  )
        units  = self.parameters.graph_db_time_units.lower()
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

        temp              = [ ( ( x - convert_offset ) * convert_factor )  for x in time_data ] # temp is new time_data

        # !! add this for energy zero self.graph_energy_zero  = "absolute" # "absolute" "first_value"
        # !! convert to named tuple
        graph_data        = ( temp, inst_pw_data, total_energy_data )

        return graph_data

# --------------------------------
if __name__ == '__main__':
        """
        run the app
        """
        import   smart_plug_graph
        a_app = smart_plug_graph.SmartPlugGraph(  )


# ===================== eof ====================================



