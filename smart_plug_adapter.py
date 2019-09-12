# -*- coding: utf-8 -*-




#import logging
#import sys
#import os
import time
#import datetime
#import traceback
#import queue
#import threading
#import importlib
import pyHS100
import sqlite3 as lite



# ----------- local imports --------------------------
#import parameters
#import gui
from   app_global import AppGlobal
#import smart_plug_helper




# ========================== Begin Class ================================
class SmartPlugAdapter( object ):
    """
    smart plug with added attributes, to adapt to this application,
    now replaces named tuple which might have been enough. ??
    """
    def __init__(self ):
        """
        try to get all declared here -- could be slots ??


        """
        # some set via parameters
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
#            label       = self.gui_tk_label
#            msg         = "failed to communicate with plug"
#            label.config( text = msg )
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
            label       = self.gui_tk_label
            label.config( text = 'timer stop' )

        else:
            self.timer_sec_left  = sec_left
            # just update display
            self.gui_tk_label.config( text = f'timer running, time left: {sec_left} plug: {self.name}' )

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
            label       = self.gui_tk_label
            label.config( text = 'plug off' )
            if self.timer_on:
                self.timer_on = False
                msg   = "Plug off and Timer Off"
                print( msg  )
                AppGlobal.gui.print_info_string( msg )
        # may save event
        except Exception as exception:             # look up correct exception
            label       = self.gui_tk_label
            msg         = "failed to communicate with plug"
            label.config( text = msg )
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
            label       = self.gui_tk_label
            label.config( text = 'plug on' )
        except Exception as exception:             # look up correct exception
            label       = self.gui_tk_label
            msg         = "failed to communicate with plug"
            label.config( text = msg )
            msg         = msg + ": " + self.name
            AppGlobal.gui.print_info_string( msg )
        # may save event

    # ----------------------------------------------
    def record_on( self, ):
        """
        call from ht or gt
        """

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
        msg   = f"record_off for: {self.name}"
        print( msg  )
        AppGlobal.gui.print_info_string( msg )
        self.recording           = False

#        self.last_record_time    = 0.
#        self.next_record_time    = time.time()     # start now
#        self.record_delta        = 10
        # may save event


    # ----------------------------------------------
    def insert_measurements( self, data ):
        """
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

# =======================================

if __name__ == '__main__':
    """
    run the app -- this may be old code, check that it is right against main app
    """
    import smart_plug
    a_app = smart_plug.SmartPlug(  )




