# -*- coding: utf-8 -*-



#    This module is mostly for things that run in the so called helper thread, ht_
#    Included are the tasks and task lists
#    !! catching too many exceptions

import time
import queue
import sys
import datetime
import threading
import smtplib       # for email
#from email.MIMEMultipart   import MIMEMultipart
#from email.MIMEText        import MIMEText

#from  email.mime.multipart.MIMEMultipart  import MIMEMultipart
#import email.mime.multipart.MIMEMultipart
from email.mime.multipart   import MIMEMultipart
from email.mime.text        import MIMEText

# ------------- local imports
from app_global import AppGlobal
#import db

# try with subclassing of Thread
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

        self.controller             = AppGlobal.controller
        AppGlobal.helper            = self
        self.parameters             = AppGlobal.parameters
        #self.scheduled_event_list   = AppGlobal.scheduled_event_list

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
    def time_polling(self):
#        print( "time_polling" )
        now   = time.time()
        for   i_timer_adapter in AppGlobal.smartplug_adapter_list :
              i_timer_adapter.poll()

    # ------------------------------------------------
    def polling(self):
        """
        started from gui this is an infinite loop monitoring the queue
        actions based on queue_to_helper and run_event
        call ht
        """
        #self.logger.debug(  "HealperThread.polling()  entered " )
        while True:
            pass
            try:
#                if self.last_time  + 10 < time.time():
#                    self.last_time = time.time()
#                    self.print_info_string(   "Time" + str( self.last_time  ) ) # + a_port )

                ( action, function, function_args ) = self.rec_from_queue()
                if action != "":
                    self.logger.debug(  "smart_terminal_helper.polling() queue: " + action + " " + str( function ) + " " + str( function_args) )  # ?? comment out
                if action == "call":
                    #print( "ht making call" )
                    sys.stdout.flush()
                    self.controller.helper_task_active  = True
                    function( *function_args )
                    self.logger.debug(  "smart_terminal_helper.polling() return running helper loop "  )  # ?? comment out
                    #self.print_helper_label( "return running helper loop " )
                    self.controller.helper_task_active  = False    # do we maintain this, or move to helper
                if action == "stop":
                    # this will kill the thread
                    self.controller.helper_task_active  = False
                    return

                self.time_polling()
#
            # must catch all exceptions if we do not want polling to fail
            except Exception as he:
                #self.logger.info( "schedule_me_helper.HelperThread threw execption from " + he.msg )        # info debug...
                self.logger.error( "schedule_me_helper.HelperThread threw exception from " + str( he ),  exc_info = True )        # info debug...
            time.sleep( self.ht_delta_t )  # ok here since it is the main pooling loop

        return

    # ------------------------------------------------
    def end_helper( self, ):
        """
        a function to interrupt the help thread and go back to polling
        function called to end the helper subroutine
        if another functin is running posting for this
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
        self.post_to_queue(  "info", None, ( text ) )  # info gui.print_info_string goes to reciev area

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

    # ------------------------------------------------
    def release_gui_untilxxxx( self, until_time ):
        """
        arg: until_time ( a time, like time.time() ) untill which the gui will be
        ret: zip
        throws: HelperException if anything comes in on queue

        released to run, if until_time = 0. then gui relaeased "forever"
        !! not implemented
        release for time, then relock, if for_time == 0.
        release "forever"
        release the main thead from its polling loop for time in float seconds
        can also call to get controller to pause again
        need to keep recieving, and keep eye on queue
        () = self.release_gui_for( time )
        also risk of lock up if controller does not respond
        have an exit with exception ??
        if exception will cause request_to_pause = False
        helper thread only
        """
        if until_time == 0.:
            self.controller.request_to_pause = False
            return

        wait_till   = until_time

        self.controller.request_to_pause = False

        while ( time.time( ) < wait_till ):

             time.sleep( .1 )
             data = self.controller.receive()  # !! FIX IS REINABLED

             if  ( self.queue_to_helper.empty() ):
                 pass
             else:
                 # ( action, function, function_args ) = self.rec_from_queue()

                 # queue_item  = self.rec_from_queue()
                 self.logger.info( "raise HelperException",  )
                 raise HelperException( 'in release_gui_for' ) #, queue_item )

        self.controller.request_to_pause = True

        if  not(   self.controller.paused ):
            time.sleep( .1 )

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
        sends some data and waits for time to recieve a reply
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

# ========================== Begin Class ================================
class ScheduledEvent( object ):
    """
    these are events that are scheduled to run at some time and then in some way
    reschedule themselfes

    sch_me.ScheduledEvent(   self, event_name, action, when, reschedule_function, rs_1 = 1. , rs_2 = 1.  )
    event to be run
    when reschedule make a new one or just use the old ones
    for now make a new one
    """
    def __init__( self, event_name      = "un named event",
                 a_parameter_dict_name  = None,
                 event_function         = None,
                 event_time             = None,
                 reschedule_function    = None,
                 rs_1 = 1. , rs_2 = 2. ):
        """

        """
        self.name                   = event_name
        self.parameter_dict_name    = a_parameter_dict_name
        self.next_run_time          = event_time
        self.event_function         = event_function
        self.reschedule_function    = reschedule_function  # a function


        # we can afford names for each so refactor to name ??
        self.reschedule_arg_1       = rs_1  # typically a count     think about fixing these names
        self.reschedule_arg_2       = rs_2  # typically a deltatime

    # -------------------------------------------
    def __str__( self ):
        """
        """
        ret =  ( self.name   +
               " a_parameter_dict_name: "     + str( self.parameter_dict_name )   +
               " next_run_time   "            + str( self.next_run_time )         +
               "\nevent_function:  "          + str( self.event_function )        +
               "\nreschedule_function:  "     + str( self.reschedule_function )   +
               "\nreschedule_arg_1:  "        + str( self.reschedule_arg_1 )      +
               "\nreschedule_arg_2:  "        + str( self.reschedule_arg_2 )
               )

        return ret

# ========================== Begin Class ================================
class ScheduledEventList( object ):
    """
    the "list" of events to be run
    and the functions to manage and run them
    """
    def __init__( self,  ):
        """
        """
        self.logger               = AppGlobal.logger
        self.reset()

    # -------------------------------------------
    def reset( self, ):
        """
        restart will reset from parameters without a recreate ??
        but all that is controlled by the controller not here
        so not clear what reset is for.
        """
        self.future_events        = []    # these are the events we will process and update
        # self.last_email           = None
        self.email_last_time      = None     # datetoime  -- change name ?
        self.email_count          = 0
        self.last_query_dt        = None
        self.last_success_dt      = None   # init to time.time() ??
        self.sig_past_events      = []     # last significant event times -- mostly fails ( later change to queue ish )
                                           # tuples, ( time, event_string )
        self.event_msg_no_connect = "failed to connect"

#        self.email_fetch_fails    = []    # time when fetch failed and email sent
#        self.email_range_fails    = []    # time when range failed and email sent
#        self.email_un_fails       = []    # things back on track and email sent

    # -------------------------------------------
    def __str__( self ):
        """
        """
        ret =  ( "ScheduledEventList"   + str( len( self.future_events ) ) )

        for i_event in self.future_events:
            pass
            str_event   = str( i_event )
            ret         += "\r" + str_event

        return ret

    # -------------------------------------------
    def run_event( self, ):
        """
        run event if its time has come ( in past actually )
        ?? catch all exceptions internally so we do not kill our polling
        add dict_name to call of each function
        """
        #print( "run event()" )
        if len( self.future_events ) == 0:
            return
        top_event        = self.future_events[0]
        if top_event.next_run_time > datetime.datetime.now():
            #AppGlobal.logger.debug( "not time" )
            return
        # need to better manage if past time ??
        # run it, replace or/delete it, add new one
        msg = str( datetime.datetime.now())  + " >>running event " + top_event.name + " parm: " + str( top_event.parameter_dict_name )
        AppGlobal.logger.debug( msg )
        AppGlobal.helper.print_info_string( msg  )
        top_event.event_function(      top_event.parameter_dict_name )
        top_event.reschedule_function( top_event.parameter_dict_name  )

        self.sort_events(  )

    # --------------------------------------------------------
    def add_event( self, a_event ):
        """
        add an event and sort for earliest first
        """
        print( "adding event..." )
        print( a_event )
        self.future_events.append( a_event )
        self.future_events.sort( key=lambda a_event: a_event.next_run_time, reverse=False )

        self.sort_events( )

    # --------------------------------------------------------
    def delete_event_0( self, ):
        """
        delete 'first' event remember to resort
        """
        del self.future_events[0]
        self.sort_events( )

    # --------------------------------------------------------
    def sort_events( self, ):
        """
        sort events, soonest at element 0
        """
        self.future_events.sort( key=lambda a_event: a_event.next_run_time, reverse=False )

#        print( "sort_events - events now:" )
#        for  i_event in self.future_events:
#            print( i_event )

   # --------------------------------------------------------
    def test_db_connect( self, a_dict_name,  ):
        """
        old does it still work in what context
        test if the db connect works
        add logging, add email
        need to limit amount of email - may need to reset that from gui
        """
        a_event         = self.future_events[ 0 ]   # or pass as an argument ??
        a_name          = a_event.name
        helper          = AppGlobal.helper

        a_db            = db.DBAccess()
        db_connect_ok   = a_db.open( a_dict_name )
        a_db.close()

#        print( "db.open ", db_connect_ok  )
        if  db_connect_ok:
            #print( "db.open ", ok  )
            msg = "db open ok "
        else:
            msg = "db failed to open "

        helper.print_info_string( "fe_db_connect: running event " + a_name  + " now = " + str( datetime.datetime.now()) +

        + "using dict named: " + a_dict_name + " " + msg )
        #self.send_email( "fe_post_message:" , "running event " + a_name   )

    # --------------- event functoin = ef -----------------------------------------
    def ef_post_message( self,  a_dict_name,  ):
        """
        event functoin = ef = use as a function in an event
        this is maily a test function just posting to gui
        consider adding some more info -- current time count......
        """
        a_event         = self.future_events[ 0 ]   # or pass as an argument ??
        a_name          = a_event.name
        helper          = AppGlobal.helper
        helper.print_info_string( "fe_post_message with email:  running event " + a_name  + " now = " + str( datetime.datetime.now())  )
        #self.send_email( "fe_post_message:" , "running event " + a_name   )   # debug

   # --------------------------------------------------------
    def ef_db_fetch_email( self,  a_dict_name, ):
        """
        event function = ef = use as a function in an event
        should be run by self.run_event
        test remote system by fetching data and sending email if allowed by rules
        this is for greenhouse and perhaps root cellar, should depend on parm name to increase the flexability
        without writing a new function
        name fe_db_fetch_email is not good
        return: oly update of state
        """
        a_dict     = AppGlobal.parameter_dicts[ a_dict_name ]               # get the dictionary for this event

#        msg        = self.fetch_recent_data( a_dict_name )                  # run helper function to get data, returns coded messages msg
#       replace above april 2018
        msg        = self.fetch_recent_data_values( a_dict_name )

        # analaze return message
        # more cases than needed, for enhancement consider optimizing later ??
        if msg.startswith( "ok" ):
            # adjust values in dict
            a_dict["failed_connect_count"]  = 0                              # we reset count if connect is now working
            AppGlobal.logger.info( "return ok so: 'failed_connect_count' set to 0" )
            return  # suppress email send which is in the fall through

        #not ok -- need to analize the reason for the failure and take action

        elif  msg.startswith( "no_db_connect"):   # increase count email if too high
            a_dict["failed_connect_count"]  += 1
            AppGlobal.logger.error( 'a_dict["failed_connect_count = "]'     + str( a_dict["failed_connect_count"] ) )
            AppGlobal.logger.error( 'a_dict["max_connect_count = "]'        + str( a_dict["max_connect_count"]    ) )
            AppGlobal.helper.print_info_string( "bad connect: count now = " + str( a_dict["failed_connect_count"] ) )
            if a_dict["failed_connect_count"] > a_dict["max_connect_count"]:
                pass   # on to email unless some already sent(checked later )
            else:
                return # supress email which is in the fall through

        elif  msg.startswith( "fetch_threw_exception" ): # treat like failed to connect
            AppGlobal.helper.print_info_string( msg )
            a_dict["failed_connect_count"]  += 1
            AppGlobal.helper.print_info_string( "fetch_threw_exception: count now = "  + str( a_dict["failed_connect_count"] ) )
            if a_dict["failed_connect_count"] > a_dict["max_connect_count"]:
                pass   # on to email unless some already sent
            else:
                return
        elif  msg.startswith( "no_recent_data" ):       # this means the data collection has failed
            AppGlobal.helper.print_info_string( msg )
            pass  # on to email the fall through

        elif  msg.startswith( "out_of_range" ):         # data in some way out of range, details in msg
            AppGlobal.helper.print_info_string( msg )
            # email if time ok
            pass # on to email
#        elif  msg.startswith( "*>bat" ):
#            pass
        else:
            # should not happen but lets catch and log while we go on to eamil
            log_msg  = "unexpected case in ef_db_fetch_email: " + msg
            AppGlobal.helper.print_info_string( log_msg )
            AppGlobal.logger.error( log_msg )

        if ( a_dict["time_last_email"] is None ) or (
                a_dict["time_last_email"]  +  a_dict["min_repeat_email_time"]  < datetime.datetime.now() ):
             pass # ok to email
        else:
             return   # suppress email even if otherwise required

        a_dict["time_last_email"]   = datetime.datetime.now()   # so we do not send again too soon but email could fail .... ??

        # compose and send message

        a_event         = self.future_events[ 0 ]   # or pass as an argument ??
        a_name          = a_event.name
        subject         = a_event.name
        mail_msg        = ( "Email >> At time: " + str( datetime.datetime.now() ) + " in event " + a_event.name +
                           "\n we got a 'bad' return = " + msg )
        AppGlobal.helper.print_info_string( mail_msg )
        AppGlobal.logger.info(              mail_msg )

        self.send_email( subject,           mail_msg )

    # --------------- ef = event function
    # -------------------------------------------
    def erf_reschedule_deltat_t( self, a_parameter_dict_name ):
        """
        erf event reschedule function = = use as a function in an event for rescheduling
        reschedule an event based just on delta t and count
        just modifies the current event, or deletes it
        this is a typical function for a_reschedule_function in an event
        this is set up in parameters.py init_from_helper()
        """
        a_event       = self.future_events[ 0 ]
        count_to_go   = a_event.reschedule_arg_1
        delt_t        = a_event.reschedule_arg_2

        if   count_to_go == 0:
            self.delete_event_0()
            AppGlobal.logger.debug( "erf_reschedule_deltat_t count_to_go == 0: deleted event " )
            return

        # we want to skip times while machine was off or asleep so we will do some math
        # want to be close to intergeral multiples of delta time from first setting
        # may be close to 0 if no sleep or off time
        skip                    = int( ( datetime.datetime.now() - a_event.next_run_time ) / delt_t )
        new_time                = ( ( skip + 1 ) * delt_t ) + a_event.next_run_time
        a_event.next_run_time   = new_time

        if count_to_go > 0:
                new_count_to_go     = count_to_go - ( skip + 1 )
                # but do not slip to negative
                if ( new_count_to_go < 0 ):    #minmax function better
                     new_count_to_go = 0
        else:
                new_count_to_go     = -1  # same as old - effectively

        a_event.reschedule_arg_1 = new_count_to_go

        print("new_time" + str( new_time ))
        msg  = "updated event" + str( self.future_events[ 0 ] )
        print( msg )

        AppGlobal.logger.debug( msg )
        AppGlobal.logger.debug( "erf_reschedule_deltat_t done" )

        AppGlobal.logger.debug( str( self ) )

    # ---------------- various helper functions ----------------------------------------
    def fetch_recent_data_values( self, a_dict_name ):
        """
        check called from self.ef_db_fetch_email
        connect and fetch some recent recent data ( records should exist )
        then check to see if fall in reasonable values
        might check all values since last check
        return a msg, ok if ok else some message -- messages are coded see caller

        """
        a_dict     = AppGlobal.parameter_dicts[ a_dict_name ]
        try:                                            # try to contain the damage if a misconfigured event blow out

            a_event         = self.future_events[ 0 ]   # the event is automagically in this position prior to
                                                        # calling this function get a reference to it here
            a_name          = a_event.name              #
            helper          = AppGlobal.helper          # what

            a_db            = db.DBAccess()             # local reference to db access object

            db_connect_ok   = a_db.open( a_dict_name )  # open the dataqbase using the named dict
            if  not( db_connect_ok):
                return "no_db_connect"                  # failed to get a connect

            fetched_data    = []                        # prepare for fetching data
            # we want a select that does not included past data,
            # sort by data value we are interested in then examine
            # stash data in instance variable or pass as an argument

            if ( self.last_query_dt == None ):
                     dt_past        = ( datetime.datetime.now() - a_dict["select_timedelat"] )
            else:
                     dt_past        = self.last_query_dt    # - AppGlobal.parameters.select_timedelat ) tweak by seconds??

            self.last_query_dt      = datetime.datetime.now()

            ts_past         = time.mktime( dt_past.timetuple() )
            #print( "ts_past  ", ts_past  )

            #sql         = "SELECT gh_time, temp_1, humid_1 FROM env_data_table_1  WHERE ( gh_time > %s ) order by temp_1 asc"
            sql         = a_dict[ "sql_select" ]

            cur         = a_db.db_connection.cursor()
            cur.execute( sql , (  ts_past  ) )

            # get rows
            got_data  = False
            while True:
               row   = cur.fetchone()
               #print( row )
#               AppGlobal.logger.debug( str( row ))
               if row is None:
                   #print( "break" )
                   break
               else:
                   #print( "got_data  = True" )
                   got_data  = True
                   fetched_data.append( row )

            if not( got_data ):
               a_db.close()
               return "no_recent_data"

            a_db.close()   # close now but data is safe in fetched_data

            # --- test for out of bounds min
            data_row   = fetched_data[0]  # first row lowest temp ??
            data_time  = data_row[0]      # for index look at query
            data_temp  = data_row[1]      # for index look at query

            test_val   =  a_dict[ "alarm_min_temp" ]
            if ( data_temp <= test_val  ):

                msg      = self.compose_hi_low_msg( "", False, data_time, data_temp, test_val, a_dict_name )

            # --- test for out of bounds max
            data_row   = fetched_data[-1] # last row highest temp ??
            data_time  = data_row[0]      # for index look at query
            data_temp  = data_row[1]      # for index look at query

            #if ( data_temp >= self.alarm_max_temp  ):
            test_val   =  a_dict[ "alarm_max_temp" ]
            if ( data_temp >= test_val ):
                msg      = self.compose_hi_low_msg( msg, True, data_time, data_temp, test_val, a_dict_name )
            msg  = "ok, but add recent values to message "
        except Exception as ex_arg:
            self.logger.error( "fetch_recent_data_values threw exception: " + str( ex_arg ) )
            # ?? need to look at which we catch maybe just rsh
#            next is ng, need to lookup this stuff
#            (atype, avalue, atraceback)   = sys.exc_info()
#            a_join  = "".join( traceback.format_list ( traceback.extract_tb( atraceback ) ) )
#            self.logger.error( a_join )

            msg = "fetch_recent_data_values threw exception"

        return msg

   # --------------------------------------------------------
    def fetch_recent_data( self, a_dict_name ):
        """
        connect and fetch some recent recent data ( records should exist )
        -- might want to expand to check data values -- this is alarm function
        might check all values since last check
        return string coding success
        """
        a_dict          = AppGlobal.parameter_dicts[ a_dict_name ]
        a_event         = self.future_events[ 0 ]   # or pass as an argument ??
        a_name          = a_event.name
        helper          = AppGlobal.helper

        a_db            = db.DBAccess()
        db_connect_ok   = a_db.open( a_dict_name )

        if  not( db_connect_ok):
            return "no_db_connect"

        #dt_past        = ( datetime.datetime.now() - AppGlobal.parameters.select_timedelat )
        dt_past        = ( datetime.datetime.now() - a_dict["select_timedelat"]  )
        ts_past         = time.mktime( dt_past.timetuple() )
        print( "ts_past  ", ts_past  )
        AppGlobal.logger.debug( "ts_past = " + str( ts_past )  )
#        dt_then         = dt_now -  datetime.timedelta( minutes = 50  )   # parameterize this ??
        #dt_then         = dt_now -  datetime.timedelta( days = 5  )   # parameterize this ??

        # sql         = "SELECT gh_time, temp_1, humid_1 FROM env_data_table_1  WHERE ( gh_time > %s ) order by gh_time asc"
        sql         = a_dict["sql_select"]
        AppGlobal.logger.debug( "sql = " + str( sql )  )
        cur         = a_db.db_connection.cursor()
        cur.execute( sql , (  ts_past  ) )

        # get rows
        got_data  = False
        while True:
           row   = cur.fetchone()

#           AppGlobal.logger.debug( "fetch_recent_data row = "  + str( row ))
           if row is None:
               break
           else:
               got_data  = True

        if not( got_data ):
           a_db.close()
           return "no_recent_data"

        a_db.close()

        return "ok"

    # --------------------------------------------------------
    def compose_hi_low_msg( self, current_msg, high_msg_flag, data_time, data_temp, data_limit  ):
        """
        compose or add to current_msg
        """
        if current_msg == "":
            msg      = "out_of_range "   # key word, beware of change, or make class instance
        else:
            msg      = current_msg + "\n"

        if high_msg_flag:
            msg      += "hit high temp limit"
        else:
            msg  += "hit low temp limit"

        msg      += " at "      + str( data_time  )
        msg      += " value = " + str( data_temp  )
        msg      += " limit = " + str( data_limit )

        return msg

    # ----------------------------------------
    def log_send_email( self, msg, subject, body ):
        """
        use to do some test on email without sending it
        """
        AppGlobal.logger.debug( msg + " Subject:  " + subject  +
                                 "\nMessage body:\n" + body )

        return

    # ----------------------------------------
    def send_email( self, subject, body  ):
        """
        send only if still allowed
        use parm file for send details -- except subject and body
        ?? split to 2 methods
        """
        #from email.MIMEMultipart import MIMEMultipart
        #from email.MIMEText import MIMEText
        #Then we compose some of the basic message headers:

        # !!!!!!!!!!!!!! only for testing
        self.log_send_email( "send_email() testing send email - actual email suppressed!!!!!!!!!", subject, body )


        return

        self.parameters = AppGlobal.parameters    # really bad way to do this

        if self.email_count >= AppGlobal.parameters.email_max_count:
            AppGlobal.logger.debug( "not sending email, reached max count " + subject )
            return

        if self.email_last_time == None:
            pass

        elif ( ( self.email_last_time + self.parameters.email_min_repeat_time ) > datetime.datetime.now() ):
            AppGlobal.logger.debug( "not sending email, too soon " + subject )
            return

        msg             = MIMEMultipart()
        msg['From']     = self.parameters.email_from_address
        msg['To']       = self.parameters.email_to_address
        msg['Subject']  = subject
        #Next, we attach the body of the email to the MIME message:
        #body            = "Python test mail this can be as long as you want just get a string, attachments have to see."
        msg.attach( MIMEText( body, 'plain') )
        #For sending the mail, we have to convert the object to a string, and then
        #use the same prodecure as above to send using the SMTP server..
        #import smtplib
        server  = smtplib.SMTP( self.parameters.email_server, self.parameters.email_port )
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login( self.parameters.email_account, self.parameters.email_account_pass  )
        text    = msg.as_string()

        #problems     = "email send may be commeted out "
        problems = server.sendmail( fromaddr, toaddr, text )
        server.quit()
        log_send_email( self, "email sent", subject, body )
        print( problems )
        AppGlobal.logger.error( " send_email() problems log: " + str( problems ) )
        self.last_email_time   = datetime.datetime.now()
        self.email_count       +=1

    # --------------------------------------------------------
    def test_query( self, ):
        """

        """
        dt_now         = ( datetime.datetime.now() )
#        dt_then         = dt_now -  datetime.timedelta( minutes = 50  )   # parameterize this ??
        dt_then         = dt_now -  datetime.timedelta( days = 5  )   # parameterize this ??

        print( "dt_then ", dt_then )
        print( "dt_now  ", dt_now  )

        a_db            = db.DBAccess()
        db_connect_ok   = a_db.open()

        if  not( db_connect_ok):
            return "no_db_connect"

        sql         = "SELECT gh_time, temp_1, humid_1 FROM env_data_table_1  WHERE ( gh_time > %s ) order by gh_time asc"
        #sql         = "SELECT gh_time, temp_1, humid_1 FROM env_data_table_1  order by gh_time asc"

        cur         = a_db.db_connection.cursor()

        # parameters seem to be datetimes
        #cur.execute( sql , ( dt_then, dt_now  ) )
        cur.execute( sql , (   ) )

        #cur.execute( sql , ( dt_now,  dt_then ) )
        # get rows one at a time in loop why, just one is enough
        got_data  = False
        while True:
           row   = cur.fetchone()
           print( row )
           AppGlobal.logger.debug( str( row ))
           if row is None:
               break
           else:
               got_data  = True

        if not( got_data ):
           a_db.close()
           return "no_recent_data"

        a_db.close()
        return "got_recent_data"


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

    import smart_plug
    a_app = smart_plug.SmartPlug(  )


# =================== eof ==============================





