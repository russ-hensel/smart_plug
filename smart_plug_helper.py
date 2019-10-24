# -*- coding: utf-8 -*-

"""
Purpose:
     This module is mostly for things that run in the so called helper thread, ht_
     of course initial call does need to be done in the main thread
     for the smart_plug.py app

     !! catching too many exceptions ??
"""

import time
import queue
import sys
#import datetime
import threading
#import smtplib       # for email

#from email.mime.multipart   import MIMEMultipart
#from email.mime.text        import MIMEText

# ------------- local imports
from app_global import AppGlobal
#import db

# try with sub classing of Thread
# or is this a thread   or just its manager
# In other words, only override the __init__() and run() methods of this class.
# class threading.Thread(group=None, target=None, name=None, args=(), kwargs={})
# If the subclass overrides the constructor, it must make sure to invoke the base class constructor (Thread.__init__()) before doing anything else to the thread.


class HelperThread( threading.Thread ):
    """
    run a second thread not blocked by the gui
    assume all methods run from the second thread unless otherwise stated
    this method will of course have to be called from the gui thread
    this object runs a polling thread looking at queue_to_helper to decide what
    to do
    """
    def __init__(                  self, group=None,  target=None,   name=None, args=(), kwargs=None,  ):
        # this may not be python 3.x
        #threading.Thread.__init__( self, group=group, target=target, name=name, verbose=verbose )   # verbose not throwing an error   say what
        # for python 3
        threading.Thread.__init__( self, group=group, target=target, name=name, )   #
        # class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)¶
        """
        call: gt
        """
        self.args                   = args
        self.kwargs                 = kwargs

        AppGlobal.helper            = self
        self.controller             = AppGlobal.controller
        self.parameters             = AppGlobal.parameters

        self.queue_to_helper        = self.controller.queue_to_helper
        self.queue_fr_helper        = self.controller.queue_fr_helper

        self.ht_delta_t             = self.parameters.ht_delta_t
        self.logger                 = AppGlobal.logger   # THIS is a short term approach ?
        self.last_time              = time.time()

        return

    # ------------------------------------------------
    def run( self ):
        """
        called when thread is started from gt its call should be considered as from ht
        """
        self.parameters.init_from_helper()

        self.scheduled_event_list   = AppGlobal.scheduled_event_list
#        AppGlobal.print_me()        # debug, take out
#        print( "==============================================" )
        self.polling()   # may mach name in gui thread

    # ------------------------------------------------
    def device_polling(self):
        """
        poll the devices - now just smartplugs, but fairly easily adapted to other polling
        tasks.
        so simple may put back in polling
        also extended for graphing
        """
#        print( "device_polling" )
        now   = time.time()
        for   i_adapter in AppGlobal.smartplug_adapter_list:
              i_adapter.poll()

        # now the live graph
#        print( f"AppGlobal.graph_live {AppGlobal.graph_live_flag}")
        if not AppGlobal.graph_live_flag:
            return
#        print( "smart_plug_helper device_polling graph_live" )
        # think this test now in graph_live
        update_graph_bool   = False
        for i_adapter in AppGlobal.smartplug_adapter_list:
            if i_adapter.graphing_new_data:
                update_graph_bool   = True
                break
#        print( f"update_graph_bool {update_graph_bool}" )
        if not update_graph_bool:
#            print( f"update_graph_bool {update_graph_bool}" )
            return

        AppGlobal.graph_live.polling()

    # ------------------------------------------------
    def polling(self):
        """
        started from gui this is an infinite loop monitoring the queue
        actions based on queue_to_helper and run_event
        application purpose is the device polling where we monitor/record the devices
        call ht
        """
#        self.logger.debug(  "HealperThread.polling()  entered " )
        while True:

            try:
#                if self.last_time  + 10 < time.time():
#                    self.last_time = time.time()
#                    self.print_info_string(   "Time" + str( self.last_time  ) ) # + a_port )

                ( action, function, function_args ) = self.rec_from_queue()
                if action != "":
                    self.logger.debug(  "smart_plug_helper.polling() queue: " + action + " " + str( function ) + " " + str( function_args) )  # ?? comment out
                if action == "call":
                    #print( "ht making call" )
                    sys.stdout.flush()
                    self.controller.helper_task_active  = True
                    function( *function_args )
                    self.logger.debug(  "smart_plug_helper.polling() return running helper loop "  )  # ?? comment out
                    #self.print_helper_label( "return running helper loop " )
                    self.controller.helper_task_active  = False    # do we maintain this, or move to helper -- looks like not used, app global better location
                if action == "stop":
                    # this will kill the thread --- think it is the return which should end the loop ?  or do we need a braak
                    # seems to be working fine, !! remove the print
                    print( "helper got stop in the queue -- how do i end the thread " )
                    self.controller.helper_task_active  = False
                    return

                self.device_polling()

            # must catch all exceptions if we do not want polling to stop ... but maybe we do
            except Exception as he:
                #self.logger.info( "schedule_me_helper.HelperThread threw exception from " + he.msg )        # info debug... !! also info to msg area
                msg   = f"smart_plug_helper.HelperThread threw exception: {he}"
                print(  f"see log: {msg}" )
                self.logger.error( msg,  exc_info = True )        # info debug...
            time.sleep( self.ht_delta_t )  # ok here since it is the main pooling loop

        return

    # ------------------------------------------------
    def end_helper( self, ):
        """
        !! never needed or used ??
        a function to interrupt the help thread and go back to polling
        function called to end the helper subroutine
        if another function is running posting for this
        will cause it to throw an exception
        ends request_to_pause
        helper thread only
        call ht
        """
        self.print_helper_label( "end_helper " )
        #self.helper_label.config( text = "test_ports testing ports" )
        #self.print_info_string( "Helper Stopped" )
        #self.post_to_queue(  "info", None, ( "Helper Stopped", ) )
        msg = "end_helper( ) Helper interrupted"
        self.print_info_string( msg )    # rec send info
        self.logger.debug( msg )

    # ------------------------------------------------
    def print_info_string( self, text ):
        """
        print info string using the queue, so thread safe
        call ht
        """
        self.post_to_queue(  "info", None, ( text ) )  # info gui.print_info_string goes to message area

        return

    # ------------------------------------------------
    def sleep_ht_with_msg_for( self, for_time,  msg, repeat_time, show_time ):
        """
        count down a time, with a message every repeat_time to gui
        """
        time_left  = for_time
        # message here
        while( True ):
            show_msg = msg + " ( time left: " + str( time_left) + ")"
            self.print_info_string( show_msg )
            if  time_left > repeat_time:
                 self.sleep_ht_for( repeat_time )
                 time_left   -= repeat_time
            elif time_left > 10.:
                 self.sleep_ht_for( time_left  )
                 time_left   = 0
            else:
                 return

    # ------------------------------------------------
    def sleep_ht_for( self, for_time ):
        """
		probably left over code
        this is a way to pause action in the ht while keeping
        recieve active
        have it end if anything is recieved??
        args: for_time number of seconds to stay here
        call ht
        """
        wait_till   = time.time( ) + for_time
        while ( time.time( ) < wait_till ):

             time.sleep( self.ht_delta_t  )
             #data = self.receive()   # this data will be printed but lost to this thread

             if  ( self.queue_to_helper.empty() ):   # this is used to break out of loop
                 pass
             else:
                 self.logger.info( "raise HelperException",  )
                 raise HelperException( 'in sleep_ht_for - queue not empty breaking back to helper thread polling ...' ) #, queue_item )

        return

    # --------------------------------------------------
    def rec_from_queue( self, ):
        """
        call from helper only, is looked for in the method run when polling.
        get item from queue if any.
        ret: tuple as below, if action == "" then nothing rec from queue
        ( action, function, function_args ) = self.rec_from_queue()
        call ht
        """
        # why not use Queue.empty() bool function ?? in code below have wrong kind of exception
        # got error  except Queue.Empty:  AttributeError: 'NoneType' object has no attribute 'Empty'
        is_empty = False
        try:
            action, function, function_args   = self.queue_to_helper.get_nowait()
        except queue.Empty:
            action          = ""
            function        = None
            function_args   = None
            is_empty        = True

        if not( is_empty ):
            self.logger.debug( "in helper, rec_from_queue  " + action + " " + str( function ) + " " + str( function_args) )  # ?? comment out

        return ( action, function, function_args )

    # -------------------------------------------------------
    def send_receive( self, send_data, for_time  ):
        """
        probably dead for this app ??
        sends some data and waits for time to receive a reply
        (       )

        ?? add flag to control throwing of exception  or message for exception
        sends a string, recieves a string, in meantime checks queue

        receive data via the comm port
        display data
        rec_data = helper.send_receive( send_data, for_time  )
        for_time is the max time else throw exception

        after timeout then throw exception
        call:    helper thread only
        args:    sends send_data, waits max time = for_time
        returns: recieved_data or  "" if times out  no throw exception if times out
        throws:  HelperException if queue is not empty
        -----
        receive only full strings ending with /n else
        accumulated in the driver /n is stripped
        call: ht
        ret:  non empt string or throws exception
        """
        #self.logger.info( "helper: send_receive() entered",  )
        wait_till   = time.time( ) + for_time

        # ?? note fix up
        #self.controller.send( send_data )      # causing a problem, post to queue ??
        self.controller.com_driver.send( send_data )
        self.post_to_queue(  "send", None, ( send_data, ) )   # ?? beware may not actually send so send above

        while ( time.time( ) < wait_till ):

             time.sleep( self.ht_delta_t  )  # ok because we are checkin recieve and queue
             # use of controller.recieve ng use only self.recieve     feb 2017
             # data = self.controller.receive()
             # data = self.receive()
             data = ""   # remove the recieve code
             if not( data == "" ):
                 return data

             if  ( self.queue_to_helper.empty() ):
                 pass
             else:
                 # ( action, function, function_args ) = self.rec_from_queue()
                 # queue_item  = self.rec_from_queue()
                 self.logger.info( "raise HelperException in send_receive",  )
                 raise HelperException( 'in send_receive' ) #, queue_item )
        self.logger.info( "send_receive() timeout",  )
        return ""  # timeout

    # --------------------------------------------------
    def post_to_queue( self, action, function, args ):
        """
                post args to the queue to the controller
        call from: helper thread
        args: action=string, function=a function, args=tuple of arguments to function
        ret: zip

        example uses:
        self.post_to_queue(  action, function, args_as_tuple )
        self.post_to_queue(  action, function, arg_a_string )   # ok will be converted to a tuple
        self.post_to_queue(  "call", function, args_as_tuple )
        self.post_to_queue(  "rec",  None, ( "print me", ) )    # rec send info
        self.post_to_queue(  "send", None, ( "print me", ) )
        self.post_to_queue(  "info", None, ( "print me", ) )    # rec send info
        """
        # convert to make calling more flexible esp
        if type( args ) is str:
            args = ( args, )

        loop_flag          = True
        ix_queue_max       = 100
        self.ix_queue      = 0   # why instance
        # self.release_gui_for( .0 )
        while loop_flag:
            loop_flag      = False
            self.ix_queue  += 1
            try:
                #print( "try posting " + action + " args= " + str( args ) )
                self.queue_fr_helper.put_nowait( ( action, function, args ) )
            except queue.Full:
                # try again but give polling a chance to catch up
                print( "helper queue full looping" )
                self.logger.error( "helper post_to_queue()  queue full looping: " +str( action ) )
                # protect against infinit loop if queue is not emptied
                if self.ix_queue > ix_queue_max:
                    #print "too much queue looping"
                    self.logger.error( "helper post_to_queue() too much queue looping: " +str( action )  )
                    pass
                else:
                    loop_flag = True
                    time.sleep( self.parameters.queue_sleep )   # ??

# ================= Class =======================
# Define a class is how we crash out
class HelperException( Exception ):
    """
    raise if in call and get another item in queue
    """
    # ----------------------------------------
    def __init__(self, msg, ): # queue_item ):
        # call ancestor ??
        # Set some exception information
        # currently pretty much a test
        self.msg         = msg    # string message
        #self.queue_item  = queue_item

# ==================  module functions


# ==============================================
if __name__ == '__main__':
    """
    run the app here for convenience of launching
    """
    print( "" )
    print( " ========== starting SmartPlug from parameters.py ==============" )

    import  smart_plug
    a_app = smart_plug.SmartPlug(  )


# =================== eof ==============================





