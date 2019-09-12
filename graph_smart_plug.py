# -*- coding: utf-8 -*-

"""
 this is the module that actually does the smart plug graphing



"""

import matplotlib.pyplot as plt     # plotting stuff

#from mpl_toolkits.axes_grid1 import host_subplot
#import mpl_toolkits.axisartist as AA
#import matplotlib.pyplot as plt

#import pylab
import logging
import time
import datetime
import sqlite3 as lite

# --------- local imports
from   app_global import AppGlobal
import parameters
import line_style




# ========================== Begin Class ================================
class Grapher:

    def __init__(self, ):
        #self.controller     = AppGlobal.controller
        self.parameters     = parameters.Parameters()
        #self.parameters     = AppGlobal.parameters
        AppGlobal.graphing  = self
        print(AppGlobal.parameters )
        print( self.parameters )
        #self.myLogger       = aController.myLogger
        self.logger         = logging.getLogger( AppGlobal.parameters.logger_id + ".sp_graph")
        self.logger.info("in GraphDB") # logger not currently used by here
        self.line_style   = line_style.LineStyle()
        #self.time_data    = None

        #self.db             = self.controller.db

    # ---------------------------------------
    def do_graph( self, db_device_adapters, ts_begin, ts_end  ):
        """
        fetch data from database print and do a simple graph
        this interfaces back to the controller, the rest do not
        """


#        self.graph_4( db_device_adapter, ts_begin, ts_end, min_points = 10 )
#        self.graph_many( db_device_adapters[0], ts_begin, ts_end, min_points = 10 )
        self.graph_many_really( db_device_adapters, ts_begin, ts_end, min_points = 10 )
        #self.graph_3( db_device, db_start, db_end )
        #self.graph_2( db_device, db_start, db_end )

    # ---------------------------------------
    def graph_4( self, db_device_adapter,  db_start, db_end, min_points ):
        """
        ( db_start, db_end  -> ) db_start and db_end are both tuples  -- used to be
        [ 0] date in string forma     [1] a timestamp
        call only from testGraph

        """
        time_data, inst_pw_data, total_power_data,    = self.prep_data( db_device_adapter.name,  db_start, db_end, min_points  )
        if time_data is None:
            return

        min_time_data     = time_data[0]
        max_time_data     = time_data[-1]

        # ------------------- now plot new ------
        # may be that this is way of multiple plots on one canvas -- but here works for one plot
        #how to set figure size ?/

        #plt.figure( plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) )) ) us this get two graphs

        fig, ax1 = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )

        #fig( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) error
        # !!need overall title
        color    = 'tab:red'


        ax1.set_title( f"Power and Energy for Device: {db_device}" );

        ax1.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}")


        ax1.set_ylabel(  "Power (Watts)", color=color )   # done in next line seems not to work
        ax1.plot( time_data, inst_pw_data,         linestyle='--', marker='x', color='y', ) # label= "Power (Watts)" )
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim( self.parameters.graph_inst_power_min, self.parameters.graph_inst_power_max )
        ax1.legend(['Power'])
        ax1.legend( loc = 2 )  # what mean location

        # ------ second graph energy
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'

        ax2.set_ylabel( "Energy (watt * hr)", color=color)  # we already handled the x-label with ax1
        ax2.set_ylim(  self.parameters.graph_total_power_min, self.parameters.graph_total_power_max )

        ax2.plot( time_data, total_power_data, linestyle='--', marker='o', color='g', label= "Energy (Watts*hr)")

        ax2.tick_params( axis='y', labelcolor=color )

        ax2.legend(['ax2 Total Energy legend'])
        ax2.legend( loc = 1 )

        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) gives second plot empty

        plt.show()

    # ---------------------------------------
    def graph_many( self, db_device_adapter,  db_start, db_end, min_points ):
        """
        still testing
        ( db_start, db_end  -> ) db_start and db_end are both tuples  -- used to be
        [ 0] date in string forma     [1] a timestamp
        call only from testGraph
         .
        """
        time_data, inst_pw_data, total_power_data,    = self.prep_data( db_device_adapter,   db_start, db_end, min_points  )
        if time_data is None:
            return

        min_time_data     = time_data[0]
        max_time_data     = time_data[-1]

        # ------------------- now plot new ------
        # may be that this is way of multiple plots on one canvas -- but here works for one plot
        #how to set figure size ?/

        #plt.figure( plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) )) ) us this get two graphs

        fig, ax1 = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )

        #fig( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) error
        # !!need overall title
        color    = 'tab:red'


        ax1.set_title( f"Power and Energy" );

        ax1.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}")


        ax1.set_ylabel(  "Power (Watts)", color=color )   # done in next line seems not to work
        ax1.plot( time_data, inst_pw_data,         linestyle='--', marker='x', color='y', label = "label1" ) # label= "Power (Watts)" )
        ax1.tick_params(axis='y', labelcolor=color)
        ax1.set_ylim( self.parameters.graph_inst_power_min, self.parameters.graph_inst_power_max )


        inst_pw_data = [ ( x/2 ) for x in inst_pw_data ]
        ax1.plot( time_data, inst_pw_data,         linestyle='--', marker='.', color='green', label = "label2" ) # label= "Power (Watts)" )

#        ax1.legend(['Power'])   # having trouble with this
#        ax1.legend( loc = 2 )  # what mean location

        ax1.legend( loc = 2 )

        # ------ second graph energy

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'

        ax2.set_ylabel( "Energy (watt * hr)", color=color)  # we already handled the x-label with ax1
        ax2.set_ylim(  self.parameters.graph_total_power_min, self.parameters.graph_total_power_max )

        ax2.plot( time_data, total_power_data, linestyle='--', marker='o', color='g', label= "Energy (Watts*hr)")

        ax2.tick_params( axis='y', labelcolor=color )

        ax2.legend(['ax2 Total Energy legend'])
        ax2.legend( loc = 1 )

        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) gives second plot empty

        plt.show()

    # ---------------------------------------
    def graph_many_really ( self, db_device_adapters,  db_start, db_end, min_points ):
        """
        still testing
        ( db_start, db_end  -> ) db_start and db_end are both tuples  -- used to be
        [ 0] date in string forma     [1] a timestamp
        call only from testGraph
         .
        """
        self.line_style.reset()
        # prep data

        for i_device_adapter in db_device_adapters:
                #time_data, inst_pw_data, total_power_data,    = self.prep_data( i_device_adapter,  db_start, db_end, min_points  )
                i_device_adapter.retrived_data_cache  = self.prep_data( i_device_adapter,  db_start, db_end, min_points  )

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

        fig, ax1 = plt.subplots( figsize=( self.parameters.graph_x_size , self.parameters.graph_y_size ) )
        color    = 'tab:red'

        ax1.set_title( f"Power and Energy for Device SmartPlugs" );
        ax1.set_xlabel( f"Time in {self.graph_time_units} from {self.graph_time_zero}")

        ax1.set_ylabel(  "Power (Watts)", color=color )   # done in next line seems not to work

        for i_device_adapter in db_device_adapters:
            self.line_style.get_next_style()
            time_data, inst_pw_data, total_power_data,  = i_device_adapter.retrived_data_cache
            ax1.plot( time_data, inst_pw_data,          linestyle = self.line_style.line_style,
                                                        marker    = self.line_style.marker_style,
                                                        color     = self.line_style.color_style,
                                                        label     = "label1" ) # label= "Power (Watts)" )

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
        ax2.set_ylim(  self.parameters.graph_total_power_min, self.parameters.graph_total_power_max )

        for i_device_adapter in db_device_adapters:
            self.line_style.get_next_style()
            time_data, inst_pw_data, total_power_data,  = i_device_adapter.retrived_data_cache
            ax2.plot( time_data, total_power_data,      linestyle = self.line_style.line_style,
                                                        marker    = self.line_style.marker_style,
                                                        color     = self.line_style.color_style,
                                                        label     = "Energy (Watts*hr)")  # label= "Power (Watts)" )


        ax2.tick_params( axis='y', labelcolor=color )

        ax2.legend(['ax2 Total Energy legend'])
        ax2.legend( loc = 1 )

        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        #plt.figure( figsize = ( self.parameters.graph_x_size , self.parameters.graph_y_size ) ) gives second plot empty

        plt.show()

    # ---------------------------------------
    def export_csv( self, db_device_adapter,  db_start, db_end, min_points = 10, csv_file_name = "data.csv" ):
        """
        needs update !! will throw error
        ?? file name check
        add sep to parameters ??
        add csv file to parameters
        ?? more title stuff
        """
        sep     = "\t"
        time_data, inst_pw_data, total_power_data,    = self.prep_data( db_device,  db_start, db_end, min_points  )

        if time_data is None:
            return

        with open( csv_file_name, "w" ) as a_file:
            a_file.write( f'"time_data"{sep}"inst_pw_data"{sep}"total_power_data"\n' )
            for ix_list, i_time in enumerate( time_data ):
                a_file.write( f"{time_data[ ix_list ]}{sep}{inst_pw_data[ ix_list ]}{sep}{total_power_data[ ix_list ]}\n" )


# --------------------------------

    def prep_data( self, db_device_adapter,  db_start, db_end, min_points  ):
        """
        !! min points not implemented
        !! allow multiple devices ??
        fetch from db and transform as per parameters
        return data in a tuple each element a list
        load some graph lables in instance variables for graph use  -- or move to return, perhaps named tuple
        """
        self.logger.debug( f"prep_data {db_start}, {db_end}" )

#        set_zero           = self.parameters.graph_time_zero  #      "max"   # min max
#        units              = self.parameters.graph_time_units     # "hour"   #  day hour  use my converter in future

        db_device_name           = db_device_adapter.name
        time_data                = []      # raw data on time may be timestamp......

        inst_pw_data             = []      #
        total_power_data         = []      #

#         ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_power )

        sql         = ( "SELECT plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_power " +
                      " FROM plug_measurements   WHERE ( plug_time > ? ) AND ( plug_time < ? ) AND ( plug_name = ? ) order by plug_time asc" )

        a_datetime_begin     = datetime.datetime.fromtimestamp( db_start )
        print( f"a_datetime_begin = { type(a_datetime_begin)}  {a_datetime_begin} " )

        a_datetime_end     = datetime.datetime.fromtimestamp( db_end )
        print( f"a_datetime_end = { type(a_datetime_end)}  {a_datetime_end} " )

        sql_con = lite.connect( AppGlobal.parameters.db_file_name )

        with sql_con:
            cur = sql_con.cursor()

            cur.execute( sql , ( db_start, db_end, db_device_name ) )

            # get rows one at a time in loop
            while True:
               row   = cur.fetchone()

               if row is None:
                   break
               print( f"{row}   [1] {row[1]}   {row[6]}" )

               time_data.append(           row[1] )
               inst_pw_data.append(        row[6] )
               total_power_data.append(    row[7] )

        msg   =   f"data points fetched: {len( time_data )}"
        print( msg )
        self.logger.info( msg )

        if  len( time_data ) < 10:
             print( "not enough data to graph" )  # add gui message
             return( None, None, None )

        temp          = []     # temporary to build new time data will put back

        zero   = self.parameters.graph_time_zero.lower()
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
        units  = self.parameters.graph_time_units.lower()
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

         # ((float(9)/5)*x + 32)
        temp  = [ ( ( x - convert_offset ) * convert_factor )  for x in time_data ] # temp is new time_data

        graph_data        = ( temp, inst_pw_data, total_power_data )

        return graph_data

        # or
        #self.time_data          = temp
        #self.inst_pw_data       = inst_pw_data
        #self.total_power_data   = total_power_data
# --------------------------------
if __name__ == '__main__':
        """
        run the app -- right now this
        """
        import   smart_plug_graph
        print( "not adjusted for the new software config " )
#        a_app = GraphDB(  )
#        a_app = a_app.do_graph(  "device_1",  1467116425, 2566956343,   )
        a_app = smart_plug_graph.SmartPlugGraph(  )


# ===================== eof ====================================

