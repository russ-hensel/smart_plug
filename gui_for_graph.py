# -*- coding: utf-8 -*-
#
# gui    for SmartPlugGraph


import logging
from   tkinter import *   # is added everywhere since a gui assume tkinter namespace
from   tkinter import ttk
import sys
from   tkcalendar import Calendar, DateEntry
import datetime
from   tkinter.filedialog import askopenfilename

#------- local imports
from   app_global import AppGlobal


#class RedirectText(object):
#    """
#    simple class to let us redirect console prints to our recieve area
#    http://www.blog.pythonlibrary.org/2014/07/14/tkinter-redirecting-stdout-stderr/
#    think no longer used
#    """
#    #----------------------------------------------------------------------
#    def __init__(self, text_ctrl):
#        """Constructor
#        text_ctrl text area where we want output to go
#        """
#        self.output = text_ctrl
#
#    #----------------------------------------------------------------------
#    def write(self, string):
#        """"""
#        self.output.insert( END, string )
#        # add scrolling?
#        self.output.see( END )
#
#        #self.myRecText.insert( END, adata, )
#        #self.myRecText.see( END )
#
#    #--------------------------------
#    def flush(self, ):
#        """
#        here to mimic the standard sysout
#        does not really do the flush
#        """
#        pass

# ======================= begin class ====================
class GUI:
    """
    gui for the application
    """
    def __init__( self,  ):
        """
        """
        AppGlobal.gui           = self
        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.root               = Tk()
        self.win                = self.root

        if self.parameters.os_win:
            # icon may cause problem in linux for now only use in win
            # print "in windows setting icon"
            #self.root.iconbitmap( self.parameters.icon )
            pass

        a_title   = self.controller.app_name + " version: " + self.controller.version + " Mode: " +self.parameters.mode
        if self.controller.parmeters_x    != "none":
            a_title  += " parameters=" +   self.controller.parmeters_x

        self.root.title( a_title )

        self.root.geometry( self.parameters.win_geometry )

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")
        self.logger.info("in class gui_new GUI init") # logger not currently used by here

        self.save_redir          = None

        self.save_sys_stdout     = sys.stdout

        self.max_lables          = 6   # number of lables, normally used for parameters
        self.lables              = []  # lables normally for parameters

        self.rb_var              = IntVar() #Tk.IntVar()

        #------ constants for controlling layout ------
        self.button_width         = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

#        self.buttons_frame_padx   = "3m"
#        self.buttons_frame_pady   = "2m"
#        self.buttons_frame_ipadx  = "3m"
#        self.buttons_frame_ipady  = "1m"

        next_frame       = 0    # position row for frames

        self.root_b      = Frame( self.root )   # this may be an extra unneded frame

        #self.root.grid( column=1, row=1 )  # this seems to set up the col grid in the root
        #self.root.pack( expand = True, sticky = E+W )  # this also works, why needed? sticky not an option here

        # this frame self.root may be rudundant with its parent
        self.root_b.grid(  column=0,row=0, sticky= E+W+N+S )
        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
        self.root.grid_rowconfigure(    0, weight=1 )

        a_frame  = self.make_query_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame  = self.make_device_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame  = self.make_db_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame = self.make_button_frame( self.root_b,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
        next_frame += 1

        self.root_b.grid_columnconfigure( 0, weight=1 )
        self.root_b.grid_rowconfigure(    0, weight=0 )
        self.root_b.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

    #------ build frames  ------------------------
        # ------------------------------------------
    def make_device_frame( self, parent, ):
        """
        device frame, list devices
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg ="gray", relief=RAISED, borderwidth=1 )

        rowspan    = 2

        for ix, i__smartplug in enumerate(  AppGlobal.smartplug_adapter_list ) :
            lcol      = 0
            lrow      = ix
            #a_widget  = Button( a_frame , width=10, height=2, text = i__smartplug_dict[ "name" ] )

            cb_var = IntVar() # how to get

            a_widget = Checkbutton( a_frame, text = i__smartplug.name,  variable = cb_var, ) # add later command=cb_cb )

            i__smartplug.gui_tk_checkbox        = a_widget  # maybe drop not sure if used
            i__smartplug.gui_tk_checkbox_var    = cb_var

            #callback=lambda x=x: f(x)
            # a_button.device_id =..... but still eval a_button later
            #a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "info" ) )
            a_widget.grid( row = lrow * rowspan, column = 0, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

#            a_button  = Button( a_frame , width=10, height=2, text = "On"  )
#            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "on" ) )
#            a_button.grid( row = lrow * rowspan, column = 1, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#            lcol +=  1
#


#
#            a_widget   =  Label( a_frame, text = "12345678901234567890", justify = LEFT, anchor = W,
#                                 borderwidth = 5, relief = RAISED,  )
#            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky = E + W + N + S )
#            i_smartplug_adapter.gui_tk_label  = a_widget
#            lcol +=  1

        return a_frame

    # ------------------------------------------
    def make_db_frame( self, parent, ):
        """
        make a frame for db connect and .....
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg ="gray", relief=RAISED, borderwidth=1 )

        # add some more for db, different style, which do I like best?
        lrow   =  0
        lcol   =  0
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        bw_for_db    = FileBrowseWidget( a_frame )
        bw_for_db.grid( row = lrow, column = lcol )
        bw_for_db.set_text( AppGlobal.parameters.db_file_name )
        self.bw_for_db = bw_for_db  # save reference

        return  a_frame

    # ------------------------------------------
    def make_query_frame( self, parent, ):
        """
        make parameter frame for queries

        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg ="gray", relief=RAISED, borderwidth=1 )

        # add some more for db, different style, which do I like best?
        lrow   =  0
        lcol   =  0
        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ------------------------------------
        lrow    += 1
        ( lrow, lcol, self.lbl_start )   = self.make_label( a_frame, lrow, lcol, "start", )
        ( lrow, lcol, self.lbl_end   )   = self.make_label( a_frame, lrow, lcol, "end", )
        #( lrow, lcol, self.lbl_db_user )   = self.make_label( a_frame, lrow, lcol, "user", )

        lrow    = 0
        lcol    = 2
        cal     = DateEntry( a_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010,    bordercolor = "red",     )

        cal.grid( row=lrow, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        cal.set_date( self.parameters.graph_begin_date  )
        self.cal_begin = cal

        cal     = DateEntry( a_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2, year=2010,    bordercolor = "red",     )
        cal.grid( row = lrow +1, column=lcol, sticky=E + W + N + S )
        cal.configure( date_pattern = "yyyy/mm/dd" )
        cal.set_date( self.parameters.graph_end_date  )
        self.cal_end     = cal

#-------------------------------------

        lrow    = 0
        lcol    = 3

        #time_of_day = ( 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24,  )   # think about

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
        a_widget.set( self.parameters.graph_begin_hr )
        self.time_begin  = a_widget

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
        a_widget.set( self.parameters.graph_end_hr )
        self.time_end  = a_widget

        #------------- some of this may be added back later or not ---------------

#        lrow    = 0
#        lcol    = 4
#        a_rb   =  Radiobutton( a_frame, text = "From Parms   ",      variable = self.rb_var, value=0,  command = self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        #lrow   = 1
#        lcol   += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Last Sun",      variable = self.rb_var, value=1,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Sun - 2 ",      variable = self.rb_var, value=2,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        lrow   = 1
#        lcol   = 4
#        a_rb   =  Radiobutton( a_frame, text = "From Sun - 3  ",      variable = self.rb_var, value=3,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        #lrow    = 0
#        lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Sun - 4  ",      variable = self.rb_var, value=4,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        #lrow   = 1
#        lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Sun - 5 ",      variable = self.rb_var, value=5,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        lrow    = 0
#        lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Now - 1 ",      variable = self.rb_var, value=6,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        lrow   = 1
#        #lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Now - 3 ",      variable = self.rb_var, value=7,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )
#
#        # ------------------------------
#        lrow    = 0
#        lcol   += 1
#        #lrow    += 1
#
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = lrow, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ------------------------------
#        lrow    = 0
#        lcol   += 1
#
#        if lrow >= 2:
#                lrow   =  0
#                lcol   += 1
#
#        a_label   = ( Label( a_frame, text = "status", relief = RAISED,  )  )
#        a_label.grid( row=lrow, column=lcol, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#        self.lbl_db_status  = a_label
#
#        ( lrow, lcol, self.lbl_db_connect )   = self.make_label( a_frame, lrow, lcol, "connect", )
#        ( lrow, lcol, self.lbl_db_host )      = self.make_label( a_frame, lrow, lcol, "host", )
#        ( lrow, lcol, self.lbl_db_db )        = self.make_label( a_frame, lrow, lcol, "db", )
#        ( lrow, lcol, self.lbl_db_user )      = self.make_label( a_frame, lrow, lcol, "user", )

        return  a_frame

    # ------------------------------------------
    def make_label( self, a_frame, a_row, a_col, a_text, ):
        """
        return tuple -- or by ref do not need to , test this in templates
        return label
        increment row col
        """
        a_row    += 1
        if a_row >= 2:
                a_row   =  0
                a_col   += 1

        a_label   = ( Label( a_frame, text = a_text, relief = RAISED,  )  )
        a_label.grid( row=a_row, column=a_col, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)

        # set weight??
        return ( a_row, a_col, a_label )

    # ------------------------------------------
    def make_button_frame( self, parent, ):
            """
            make a test frame place for test stuff esp. buttons
            """
            a_frame  = Frame( parent, width=300, height=200, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )

            buttonOpen = Button( a_frame , width=10, height=2, text = "Graph" )
            buttonOpen.config( command = self.controller.cb_graph )
            buttonOpen.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Export CSV" )
            a_button.config( command = self.controller.cb_export_csv )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Define 0 DB" )
            a_button.config( command = self.controller.cb_define_db )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Query Devices" )
            a_button.config( command = self.controller.cb_test )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Log" )
            a_button.config( command = self.controller.os_open_logfile )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Edit Parms" )
            a_button.config( command = self.controller.os_open_parmfile )
            a_button.pack( side = LEFT )

            if self.controller.parmeters_x  != "none":
                a_button = Button( a_frame , width=10, height=2, text = "Edit ParmsX" )
                a_button.config( command = self.controller.os_open_parmxfile )
                a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Help" )
            a_button.config( command = self.controller.os_open_helpfile )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Restart" )
            a_button.config( command = self.controller.restart )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Test" )
            a_button.config( command = self.controller.cb_test )
            a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def get_checked_device_adapters( self ):
        """
        what it says
        return list (device_adapter..... ) or empty
        """
        device_adapter_list = []
        for i_device_adapter in AppGlobal.smartplug_adapter_list:
            # list comp
            print( f"{i_device_adapter.name} i_device_adapter.gui_tk_checkbox_var  {i_device_adapter.gui_tk_checkbox_var}")
            if i_device_adapter.gui_tk_checkbox_var.get():
                device_adapter_list.append( i_device_adapter )
        print( f"checked devices: {i_device_adapter.name} ")
        return device_adapter_list

    # ------------------------------------------
    def get_begin_end( self ):
        """
        get begin end times from the gui -- combine dates and hours
        may need to extend to date times
        return tuple (begin, end )  -- types may vary as I mess about
        """
        hour         = AppGlobal.dd_hours.index( self.time_begin.get() )
        time_begin   = datetime.time(hour = hour )
        hour         = AppGlobal.dd_hours.index( self.time_end.get() )
        time_end     = datetime.time(hour = hour )

#        my_date    = datetime.date.today()
        min_time      = datetime.time.min   # means midnight
        dt_begin      = datetime.datetime.combine(self.cal_begin.get_date(), time_begin )
        dt_end        = datetime.datetime.combine(self.cal_end.get_date(),   time_end )

        ts_begin      = dt_begin.timestamp()
        ts_end        = dt_end.timestamp()

#        a_datetime_begin     = datetime.datetime.fromtimestamp( ts_begin )
#        print( f"a_datetime_begin = { type(a_datetime_begin)}  {a_datetime_begin} " )
#
#        a_datetime_end     = datetime.datetime.fromtimestamp( ts_end )
#        print( f"a_datetime_end = { type(a_datetime_end)}  {a_datetime_end} " )

        #return( datetime.datetime( self.cal_begin.get_date() ) , datetime.datetime( self.cal_end.get_date() ) )
        return( ts_begin , ts_end  )

    # -----  functions mostly for controller  ------------------------

    def get_db_file_name( self, ):
        """
        its name, return a string
        """
        #bw_for_db.set_text     = AppGlobal.parameters.db_file_name
        return( self.bw_for_db.get_text() )


    # ----- button actions ------------------------
    # ------------------------------------------
    def doRestartButton( self, event):
        self.controller.restart()
        return

    # ------------------------------------------
    def doOpenButton( self, event):
        self.controller.open_com_driver()
        return

    # --------------- may be left over from terminal check and delete dead stuff !!---------------------------
    def doButtonText( self, event):
        """
        easy to add functions that look at the button text
        """
        btext =  event.widget["text"]

        if btext == "Graph":
            self.controller.cb_graph()
            pass

        else:
            msg   = "no action defined for: " + btext
            self.logger.error( msg )
        return

    # ---------------  end of button actions


# -----------------------------------------
class FileBrowseWidget( Frame ):
    """
    not sure why making it ino a widget is a good idea but here goes
    this is a widget that both holds a filename
    and lets you browse to a file
    how is it different from just a couple of widgets
    in your frame ... more reusable ?
    better looking or what
    see graph_smart_plug gui for a use
    """
    def __init__(self, parent ):

        #super( BrowseWidget, self ).__init__( parent, width=60, height=20, bg ="red")
        super(  ).__init__( parent, width=60, height=20, bg ="red")
        self.label_1      = Label( self, text="File: ").grid(row=1, column=0)

        self.a_string_var = StringVar()

        self.entry_1      = Entry( self , width=100,   text = "bound", textvariable = self.a_string_var )
        self.entry_1.grid( row=1, column=1 )

        self.button_2 = Button( self, text="Browse...", command = self.browse )
        self.button_2.grid( row=1, column=3 )


    # ------------------------------------------
    def browse( self ):
        Tk().withdraw()
        filename     = askopenfilename()

        if filename == "":
            return

        self.set_text( filename )
        print( f"get_text = {self.get_text()}", flush = True )

    # ------------------------------------------
    def set_text( self, a_string ):
        self.a_string_var.set( a_string )

    # ------------------------------------------
    def get_text( self, ):
        """
        get the text from the entry
        """
        a_string   =  self.a_string_var.get(  )
        return( a_string )

# =======================================

# import test_controller # no longer used

if __name__ == '__main__':
        """
        run the app
        """
        import smart_plug_graph
        a_app = smart_plug_graph.SmartPlugGraph(  )


