# -*- coding: utf-8 -*-

import datetime
import time
import os
import sqlite3 as lite
import pyHS100
import threading

#import parameters    # or use the app global one ??

# ----------- local imports --------------------------
from   app_global import AppGlobal

# ========================== Begin Class ================================
class SmartPlugAdapter( object ):
    """
    smart plug with added attributes and methods, to adapt to this application,
    coupled to AppGlobal and then perhaps to gui ......
    this is used in both smart_plug and smart_plug_graph
    """
    def __init__(self ):
        """
        try to get all declared here -- could be slots ??

        """
        # some set via parameters see parameters.py
        self.name                = None
        self.tcpip               = None
        self.plug                = None   # looks like we can create once here and use forever

        # gui interface    may be set in gui build
        self.gui_tk_label        = None
        self.gui_tk_label_2      = None   # perhaps for posting power
        self.gui_tk_combo        = None
        self.gui_tk_checkbox     = None   # perhaps graphing gui
        self.gui_tk_checkbox_var = None

        self.gui_tk_mon_checkbox_var      = None
        self.gui_tk_record_checkbox_var   = None

        self.gui_tk_on_checkbox           = None   # for on off
        self.gui_tk_on_checkbox_var       = None

        # for timer functions
        self.timer_on            = False
        self.timer_start         = None    # time.time()   timestamp
        self.time_sec            = 0
        self.time_sec_left       = 0
        self.timer_on            = False
        # could add a timer end ??

        #self.polling             = False
        self.recording           = False
        self.monitor             = False
        # self.graphing            = False

        # these times are used for both recording, monitoring, and graphing
        self.last_record_time    = None
        self.next_record_time    = 1.
        self.delta_t             = None
        self.live_graph_lines    = None       # lines on the graph, we keep for later updating
        self.live_graph_ready    = False      # set only after ready to go

        # graphing data  reset graphing data more assigment, declare
        self.reset_graphing_data()

    # ----------------------------------------------
    def poll( self, ):
        """
        terminated with prejudice
        """
        raise Exception( "do not call smart_plug_adapter poll" )

    # ---------------------------------------
    def polling_mt( self, ):
        """
        polling for the main thread ( gui thread )
        """
        msg     =   "SmartPlugAdapter.polling_mt  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

    # ---------------------------------------
    def polling_ht( self, ):
        """
        polling for the helper thread
        """
        msg     =   "SmartPlugAdapter.polling_ht  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = False  )

        self.check_timer_done()
        self.check_recording()

    # ----------------------------------------------
    def insert_event( self, ):
        """
        call from gt and ??  no longer planning to implement
        save events like on off and retrieve data
        """
        pass

    # ----------------------------------------------
    def reset_graphing_data( self, ):
        """
        fine in helper thread ok in both
        """
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = "now in smart_plug_adapter.reset_graphing_data", main = True  )
#        print( "reset_graphing_data" )

        self.gd_time             = []
        self.gd_time_adj         = []
        self.gd_power            = []
        #self.gd_power_adj        = []
        self.gd_energy           = []
        self.gd_energy_adj       = []

        self.graphing_new_data   = False
        #self.graphing                 = True
        # get rid of
#        self.live_graph_lines.set_xdata( self.gd_time_adj )
#        self.live_graph_lines.set_ydata( self.gd_power )

    # ----------------------------------------------
    def start_graph_live( self, a_ax ):
        """
        main thead
        """
#        print( f"start_graph_live in adapter {self.name} at {self.tcpip}" )
#        msg    =  f"? ? start_graph_live for device: {self.name} "
#        AppGlobal.what_thread( threading.get_ident(), msg, 20  )
        msg     =   "SmartPlugAdapter.start_graph_live  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

        if not self.monitor:
            return

        if self.gd_time_adj is None:
            self.gd_time_adj          = []
            self.gd_power             = []

        #self.reset_graphing_data()   # why bother consider keeping data !!
        #if self.live_graph_lines is None:  # or use self.live_graph_ready
        if self.live_graph_ready    == False:  # or use self.live_graph_ready
            self.live_graph_lines,     = a_ax.plot([],[], 'o',  label = self.name )   # note unpack comma -- seem to be a list of 1 element
#            msg    =  f"self.live_graph_lines created for device: {self.name} {type(self.live_graph_lines)}  {self.live_graph_lines}"
#            AppGlobal.logger.info( msg )
#            print( msg )

#           got  >>>> why a list   self.live_graph_lines: <class 'list'>  [<matplotlib.lines.Line2D object at 0x00000274E0287AC8>]
            self.linestyle, self.colorstyle, self.markerstyle, self.widthstyle  = AppGlobal.graph_live.line_style.get_next_style()
            self.live_graph_ready  = True
        # else just keep using what we have

    # ----------------------------------------------
    def update_graph_live( self, ):
        """
        call from main thread

        from graph_live but could we use our own polling  ??
        return True or False, depending on weather we were already set up

        """
        msg     =   "SmartPlugAdapter.update_graph_live  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

        msg    =  f"Adapter.update_graph_live device: {self.name}  data: {self.graphing_new_data} ready: {self.live_graph_ready}"
        AppGlobal.logger.info( msg )

        if  (not self.graphing_new_data ) or ( not self.live_graph_ready ):
            return False

        self.live_graph_lines.set_xdata( self.gd_time_adj )
        self.live_graph_lines.set_ydata( self.gd_power )

        # not sure these need to be done on every cycle but works
        self.live_graph_lines.set_linestyle( self.linestyle   )
        self.live_graph_lines.set_color(     self.colorstyle  )
        self.live_graph_lines.set_marker(    self.markerstyle )
        self.live_graph_lines.set_linewidth( self.widthstyle  )
        self.live_graph_lines.set_label( self.name)   # not currently working lacks update or.... setting legend later seemed to do it once may be enough
        self.graphing_new_data = False

        return True

   # ----------------------------------------------
    def end_graph_live( self, ):
        #print( "smart plug adapter end_graphing still need to work this out ?? delete data here " )
        self.live_graph_ready     = False
        self.reset_graphing_data()

    # ----------------------------------------------
    def end_graphing( self, ):
        """
        this may be unused junk
        """
        print( "end_graphing still need to work this out ?? delete data here " )
        self.live_graph_ready     = False
        # self.graphing            = False

    # ----------------------------------------------
    def check_recording( self, ):
        """
        call helper thread, best or ok in main -- used by smart_plug not smart_plug_graphing
        if recording then record the data in db
        for now do not assume timer is running
        call from ht polling action
        """
        msg     =   "SmartPlugAdapter.check_recording  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = False  )

        if not ( self.recording or self.monitor ):
            return

#        msg    =  f"?ht? adapter check_recording "
#        AppGlobal.what_thread( threading.get_ident(), msg, 20  )

        now = time.time(  )
        if now < self.next_record_time:   # or monitor time
            return

        self.last_record_time    = now
        self.next_record_time    = now + self.delta_t
        try:
            plug             = pyHS100.SmartPlug( self.tcpip )
            plug_data        = plug.get_emeter_realtime()

            # ?? could add plug state - on off,.....

            # id          = f"{self.name}{self.last_record_time}r"
            # print   ( f"record data {id}:{plug_data})" )
            rnd          = "%.2f"%plug_data["power"]
            msg          = f'{rnd} watts'   #!! bit of rounding would be nice here
            self.gui_tk_label_2.config( text = msg )

        except pyHS100.smartdevice.SmartDeviceException as exception:             # look up correct exception
            self.timer_on   = False
            #self.record_off()  to much messaging and will throw own error
            msg     = f"failed to communicate with plug - record off for: {self.name} {self.tcpip}"

            AppGlobal.gui.print_info_string( msg )
            return

        if  AppGlobal.graph_live_flag and self.monitor and self.live_graph_ready:
#            print( "check_recording" )
            self.graphing_new_data     = True
            #!! normalized and unnormalize data
            self.gd_time.append( self.last_record_time )
            self.gd_time_adj.append( AppGlobal.graph_live.rescale_time_function( self.last_record_time ) )  #?? make local ref??
            self.gd_power.append( plug_data["power"]    )

        if  self.recording:
            db_data   = (  (self.name, self.last_record_time,  "r",  "?", plug_data["voltage"], plug_data["current"], plug_data["power"], plug_data["total"]),  )
            self.insert_measurements( db_data )

    # ----------------------------------------------
    def check_timer_done( self, ):
        """
        for now do not assume timer is running
        call from ht polling action
        """
        msg     =   "SmartPlugAdapter.check_timer_done  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = False  )

        if not ( self.timer_on ):
            return

        now   = time.time()
        sec_left   = ( self.timer_start + self.time_sec ) - now   # could be timer_end stored
#        print( f"check_timer_done sec_left {sec_left} for plug: {self.name} " )   # debug
        if  sec_left <= 0:
            self.off()
            self.display_msg( "Timer Stop" )
        else:
            self.timer_sec_left  = sec_left
            a_string             = self.sec_to_string( sec_left )
            # just update display
            self.display_msg( f"Timer  {a_string}" )
#            self.gui_tk_label.config( text = f'timer running, time left: {sec_left} plug: {self.name}' )

    # ----------------------------------------------
    def graph_power_from_db( self,   line_style = None, ax = None ):
        """
        None default because required hence exception
        """
        msg     =   "SmartPlugAdapter.graph_power_from_db  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

        line_style.get_next_style()
        time_data    = self.gd_time_adj
        if  ( ( time_data is None ) or  len( time_data ) == 0  ):
            print( f"no data for {self.name}" )
            return
        ax.plot( time_data, self.gd_power,          linestyle = line_style.linestyle,
                                                    marker    = line_style.markerstyle,
                                                    color     = line_style.colorstyle,
                                                    label     = self.name ) # label= "Power (Watts)"

    # ----------------------------------------------
    def graph_energy_from_db( self,   line_style = None, ax = None ):
        """
        None default because required
        """
        msg     =   "SmartPlugAdapter.graph_energy_from_db  "
        AppGlobal.log_if_wrong_thread( threading.get_ident(), msg = msg, main = True  )

        line_style.get_next_style()
        time_data    = self.gd_time_adj
        if  ( ( time_data is None ) or  len( time_data ) == 0  ):
            #print( f"no data for {i_device_adapter.name}" )
            return
        ax.plot( time_data, self.gd_energy_adj,             linestyle = line_style.linestyle,
                                                            marker    = line_style.markerstyle,
                                                            color     = line_style.colorstyle,
                                                            label     = self.name    )   # "Energy (Watts*hr)")  # label= "Power (Watts)" )

    # ----------------------------------------------
    def db_select( self,  db_start, db_end, ):
        """
        could pass in sql_con already checked out
        """
        msg   = f"Preparing data for {self.name}"
        AppGlobal.gui.display_info_string( msg )
        #self.logger.debug( f"_prep_data {db_start}, {db_end}" )

        db_device_name           = self.name
        # local references faster
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
        if not( os.path.isfile( db_file_name  )):      # already checked in caller but move whole connect back there
            msg   =  f"Error: db file does not exist: {db_file_name}"
            AppGlobal.gui.display_info_string( msg )
            return

        sql_con = lite.connect( db_file_name )
        with sql_con:
            cur = sql_con.cursor()
#            print(f"db_device_name{db_device_name}")
            cur.execute( sql , ( db_start, db_end, db_device_name ) )

            while True:  # get rows one at a time in loop
               row   = cur.fetchone()

               if row is None:
                   break
#               print( f"{row}   [1] {row[1]}   {row[6]}" )

               time_data.append(           row[1] )
               inst_pw_data.append(        row[6] )
               total_energy_data.append(   row[7] )

        msg   =   f"For device {db_device_name}: data points fetched: {len( time_data )}"
        AppGlobal.gui.display_info_string( msg, update_now = True )

        # move to instance name
        self.gd_time             = time_data
        self.gd_power            = inst_pw_data
        self.gd_energy           = total_energy_data

    # ----------------------------------------------
    def adj_db_data_energy( self,   ):
        """
        always start from 0 as first energy point  -- think about including units
        self.gd_energy         >>          self.gd_energy_adj

        """
        if len( self.gd_energy )  == 0:
            convert_offset         = 0
            convert_factor         = 1.
        else:
            convert_factor         =  1.
            convert_offset         = self.gd_energy[0]
        print( f"adj_db_data_energy {convert_offset} {convert_factor}")

        self.gd_energy_adj      = [ ( ( x - convert_offset ) * convert_factor )  for x in self.gd_energy ]
#       ?? then zero old list

    # ----------------------------------------------
    def adj_db_data_time( self,  convert_function ):
        """
        from self.gd_time        to   self.gd_time_adj
        """
        self.gd_time_adj             = [ convert_function( x ) for x in self.gd_time ]

    # ----------------------------------------------
    def get_device_checked( self, ):
        """
        see if device is checked

        """
        pass

    # ----------------------------------------------
    def on( self, ):
        """
        plug on call from ht or gt
        manage exception: plug might not be there .......
        """
        try:
            plug            = pyHS100.SmartPlug( self.tcpip )
            plug.turn_on()
            self.display_msg( "Plug On" )
        except  pyHS100.smartdevice.SmartDeviceException as exception:
            msg         = "failed to communicate with plug"
            self.display_msg( msg )
            msg         = msg + ": " + self.name
            AppGlobal.gui.print_info_string( msg )
        # may save event

    # ----------------------------------------------
    def off( self, ):
        """
        off from on or from timer running, may have a conflict as this may be called from
        either thread ht or gt
        if timer is on turn it off
        """
        try:
            self.timer_on   = False
            plug            = pyHS100.SmartPlug( self.tcpip )
            plug.turn_off()
            self.display_msg( "Plug Off" )
            if self.timer_on:
                self.timer_on = False
                msg           = "Plug off and Timer Off"
#                print( msg  )
                AppGlobal.gui.print_info_string( msg )
        # may save event
        except pyHS100.smartdevice.SmartDeviceException as exception:             # look up correct exception
            msg         = "failed to communicate with plug {self.tcpip}"
            self.display_msg( msg )
            msg         = msg + ": " + self.name
            AppGlobal.gui.print_info_string( msg )

    # ----------------------------------------------
    def cb_on( self, ):
        """
        plug on call from ht or gt
        manage exception: plug might not be there .......
        """
        cb_state = self.gui_tk_on_checkbox_var
#        print( f"cb_on cb_state {cb_state.get()} " )
        if cb_state.get():
            self.on()
        else:
            self.off()

    # ----------------------------------------------
    def cb_mon( self, ):
        """

        """
        cb_state = self.gui_tk_mon_checkbox_var
#        print( f"cb_mon cb_state {cb_state.get()} " )
        if cb_state.get():
            pass
            self.monitor_on()
        else:
            pass
            self.monitor_off()

    # ----------------------------------------------
    def cb_record( self, ):
        """

        """
        cb_state = self.gui_tk_record_checkbox_var
#        print( f"cb_record cb_state {cb_state.get()} " )
        if cb_state.get():
#            pass
            self.record_on()
        else:
#            pass
            self.record_off()

    # ----------------------------------------------
    def record_on( self, ):
        """
        call from ht or gt
        """
        self.display_msg( "Record On" )
        msg   = f"record on for: {self.name}"
        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.recording           = True
        self.last_record_time    = 0.
        self.next_record_time    = time.time()     # start now
        #self.delta_t        = AppGlobal.parameters.record_delta  # may be moved into device
        # may save event

    # ----------------------------------------------
    def record_off( self, ):
        """
        call from ht or gt
        """
        self.display_msg( "Record Off" )
        msg   = f"record_off for: {self.name}"
#        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.recording           = False

    # ----------------------------------------------
    def monitor_off( self, ):
        """
        call from ht or gt
        """
        self.display_msg( "Monitor Off" )
        msg   = f"monitor_off for: {self.name}"
#        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.monitor   = False

    # ----------------------------------------------
    def monitor_on( self, ):
        """
        call from ht or gt
        """
        self.display_msg( "Monitor On" )
        msg   = f"monitor_on on for: {self.name}"
#        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.monitor             = True
        self.last_record_time    = 0.
        self.next_record_time    = time.time()     # start now
        if AppGlobal.graph_live_flag:
            self.start_graph_live( AppGlobal.graph_live.ax )

        #self.delta_t        = AppGlobal.parameters.record_delta  # may be moved into device
        # may save event

    # ----------------------------------------------
    def start_timer( self, ):
        """
        call from ht or gt
        """
        combo_contents = self.gui_tk_combo.get()
        time_sec       = self.string_to_time( combo_contents )   # or could get index and look up
        if time_sec is None:
            # factor as a function
            self.timer_on            = False
            self.on()
            msg     = f"Plug start not time limit, is on: {plug.is_on }"
            self.gui.print_info_string( msg )

        else:
            self.timer_start         = time.time()
            self.time_sec            = time_sec
            self.time_sec_left       = time_sec
            self.timer_on            = True

            self.on()
            print( f"Plug start time" )
#            msg     = f"Plug start is_on: {self.is_on }"
#            AppGlobal.gui.gui.print_info_string( msg )

   # ----------------------------------------------
    def string_to_time( self, a_string ):
        """
        convert times in gui drop down to time in units of....
        drop the string part have a sec to string function
        use index or a lookup
        """
        if a_string == "infinite": # special case None means indefinite
            return None

        splits         = a_string.split( )
        time_num       = float( splits[0] )
        if len(splits) < 2:
            time_units = "none"
        else:
            time_units = splits[1]

        print( f"splits {splits}" )
        print( f"time_num {time_num} time_units {time_units}" )

        # no analysis now of units
        sec     = time_num * 60
        return sec

#        #times = ( "infinite", .1 minute, .5, 1,  2,   3, 5, 10 )
#        if a_string == "infinite":
#            return None
#
#        sec   = float( a_string ) * 60
#
##        print( "fix string to time and combo box....  " )
#        return  sec

   # ----------------------------------------------
    def sec_to_string( self, sec ):
        """
        take seconds to a minute time string, rounded to nearest second
        """
        min       = int( sec /60 )
        int_sec   = int( sec - min * 60 )
        a_string  = f"{min} min {int_sec} sec"
        return a_string

    # ----------------------------------------------
    def insert_measurements( self, data ):
        """
        insert data into the db
        call from ht
        data tuple of tuples or similar
        add smart filtering from greenhouse monitor
        """
        # db_file_name    = AppGlobal.gui.bw_for_db.get_text()
        # !! make connect an app global thing ??
        db_file_name   = AppGlobal.gui.get_db_file_name()
        msg    = f"insert_measurements into {db_file_name} >> {data}"
        print( msg )
        AppGlobal.gui.print_info_string( msg )

        sql_con = lite.connect( db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            # in past errors did not show
            cur.executemany( "INSERT INTO plug_measurements " +
                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy ) VALUES  " +
                       " ( ?,         ?,         ?,             ?,          ?,       ?,       ?,          ?  ) " , data  )   # could count the cols

            sql_con.commit()

    # ----------------------------------------------
    def display_msg( self, msg ):
        """
        msg in the label area

        """
        #msg   = ( msg + ( 100 * " " ) )[0:30]   # seems not to be necessary
        self.gui_tk_label.config( text = msg )

# =======================================

if __name__ == '__main__':
    """
    run the app -- this may be old code, check that it is right against main app
    """
    import  smart_plug
    a_app = smart_plug.SmartPlug(  )







