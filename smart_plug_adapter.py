# -*- coding: utf-8 -*-




import time
import pyHS100
import sqlite3 as lite

# ----------- local imports --------------------------
#import parameters

from   app_global import AppGlobal


# ========================== Begin Class ================================
class SmartPlugAdapter( object ):
    """
    smart plug with added attributes and methods, to adapt to this application,
    """
    def __init__(self ):
        """
        try to get all declared here -- could be slots ??

        """
        # some set via parameters see parameters.py
        self.name                = None
        self.tcpip               = None
        self.plug                = None   # looks like we can create once here and use forever

        # may be set in gui build
        self.gui_tk_label        = None
        self.gui_tk_combo        = None
        self.gui_tk_checkbox     = None   # perhaps graphing gui
        self.gui_tk_checkbox_var = None

        # for timer functions
        self.timer_start         = None    # time.time()   timestamp
        self.time_sec            = 0
        self.time_sec_left       = 0
        self.timer_on            = False
        # could add a timer end ??

        #self.polling             = False
        self.recording           = False
        self.last_record_time    = None
        self.next_record_time    = 1.
        self.record_delta        = 10

        self.timer_on            = False

        self.retrived_data_cache = None   # will be a list of lists or something similar, set back to None when done with data

    # ----------------------------------------------
    def poll( self, ):
        """
        poll called from ht to poll devices for actions
        """
        self.check_timer_done()
        self.check_recording()

    # ----------------------------------------------
    def insert_event( self, ):
        """
        call from gt and ??
        save events like on off and retrieve data
        """
        pass

    # ----------------------------------------------
    def check_recording( self, ):
        """
        for now do not assume timer is running
        call from ht polling action
        """
        if not ( self.recording ):
            return

        now = time.time(  )
        if now < self.next_record_time:
            return

        self.last_record_time    = now
        self.next_record_time    = now + self.record_delta
        try:
            plug             = pyHS100.SmartPlug( self.tcpip )
            plug_data        = plug.get_emeter_realtime()

            # ?? could add plug state - on off,.....

            # id          = f"{self.name}{self.last_record_time}r"
            # print   ( f"record data {id}:{plug_data})" )
        except Exception as exception:             # look up correct exception
            self.timer_on   = False
            #self.record_off()  to much messaging and will throw own error
            msg     = f"failed to communicate with plug - record off for: {self.name}"

            AppGlobal.gui.print_info_string( msg )
            return

        db_data   = (  (self.name, self.last_record_time,  "r",  "?", plug_data["voltage"], plug_data["current"], plug_data["power"], plug_data["total"]),  )

        self.insert_measurements( db_data )

     # ----------------------------------------------
    def check_timer_done( self, ):
        """
        for now do not assume timer is running
        call from ht polling action
        """
        if not ( self.timer_on ):
            return

        now   = time.time()
        sec_left   = ( self.timer_start + self.time_sec ) - now   # could be timer_end stored
        print( f"check_timer_done sec_left {sec_left} for plug: {self.name} " )   # debug
        if  sec_left <= 0:
            self.off()
            self.display_msg( "Timer Stop" )
        else:
            self.timer_sec_left  = sec_left
            a_string             = self.sec_to_string( sec_left )
            # just update display
            self.display_msg( f"Timer  {a_string}" )
            #self.gui_tk_label.config( text = f'timer running, time left: {sec_left} plug: {self.name}' )

    # ----------------------------------------------
    def off( self, ):
        """
        off from on or from timer running, may have a conflict as  this may be called from
        either thread ht or gt
        if timer is on trun it off
        """
        try:
            self.timer_on   = False
            plug            = pyHS100.SmartPlug( self.tcpip )
            plug.turn_off()
            self.display_msg( "Plug Off" )
            if self.timer_on:
                self.timer_on = False
                msg   = "Plug off and Timer Off"
#                print( msg  )
                AppGlobal.gui.print_info_string( msg )
        # may save event
        except Exception as exception:             # look up correct exception
            msg         = "failed to communicate with plug"
            self.display_msg( msg )
            msg         = msg + ": " + self.name
            AppGlobal.gui.print_info_string( msg )

    # ----------------------------------------------
    def get_device_checked( self, ):
        """
        see if device is checked

        """

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
        except Exception as exception:             # look up correct exception
            msg         = "failed to communicate with plug"
            self.display_msg( msg )
            msg         = msg + ": " + self.name
            AppGlobal.gui.print_info_string( msg )
        # may save event

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
        self.record_delta        = 10
        # may save event

    # ----------------------------------------------
    def record_off( self, ):
        """
        call from ht or gt
        """
        self.display_msg( "Record Off" )
        msg   = f"record_off for: {self.name}"
        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.recording           = False

#        self.last_record_time    = 0.
#        self.next_record_time    = time.time()     # start now
#        self.record_delta        = 10
        # may save event
    # ----------------------------------------------
    def start_timer( self, ):
        """
        call from ht or gt
        """
        combo_contents = self.gui_tk_combo.get()
        time_sec  = self.string_to_time( combo_contents )   # or could get index and look up
        if time_sec is None:
            # factor as a function
            self.on()
            msg     = f"Plug start not time limit , is on: {plug.is_on }"
            self.gui.print_info_string( msg )

        else:
            # move into device_adapter
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
        use index or a loolup
        """

        #times = ( "infinite", .1, .5, 1,  2,   3, 5, 10 )
        if a_string == "infinite":
            return None

        sec   = float( a_string ) * 60

#        print( "fix string to time and combo box....  " )
        return  sec

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
        msg    = f"insert_measurements  {data}"
        print( msg )
        AppGlobal.gui.print_info_string( msg )
        sql_con = lite.connect( AppGlobal.parameters.db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            # in past errors did not show
            cur.executemany( "INSERT INTO plug_measurements " +
                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_power ) VALUES  " +
                       " ( ?,         ?,         ?,             ?,          ?,       ?,       ?,          ?  ) " , data  )   # could count the cols

    # ----------------------------------------------
    def display_msg( self, msg ):
        """
        msg in the lable area

        """
        #msg   = ( msg + ( 100 * " " ) )[0:30]   # seems not to be necessary
        self.gui_tk_label.config( text = msg )

# =======================================

if __name__ == '__main__':
    """
    run the app -- this may be old code, check that it is right against main app
    """
    import smart_plug
    a_app = smart_plug.SmartPlug(  )




