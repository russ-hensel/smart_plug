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
from   tkinter.filedialog import asksaveasfile
import pyperclip
import ctypes

#------- local imports
from   app_global import AppGlobal

# ======================= begin class ====================
class GUI:
    """
    gui for the application
    """
    def __init__( self,  ):
        """
        build the application GUI
        """
        AppGlobal.gui           = self
        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.root               = Tk()

        a_title   = self.controller.app_name + " version: " + self.controller.version + " Mode: " +self.parameters.mode
        if self.controller.parmeters_x    != "none":
            a_title  += " parameters=" +   self.controller.parmeters_x

        self.root.title( a_title )
        self.root.geometry( self.parameters.win_geometry )

        if self.parameters.os_win:
            # from qt - How to set application's taskbar icon in Windows 7 - Stack Overflow
            # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105

            icon = self.parameters.icon_graph
            if not( icon is None ):
                print( "set icon "  + str( icon ))
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon)
                self.root.iconbitmap( icon )
            else:
                print( "no icon for you!"  + str( icon ))

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")
        self.logger.info("in class gui_new GUI init") # logger not currently used by here

        # next leftover values may not be used
        self.save_redir          = None
        self.save_sys_stdout     = sys.stdout

        self.max_lables          = 6   # number of labels, normally used for parameters
        self.lables              = []  # labels normally for parameters

        self.rb_var              = IntVar() #Tk.IntVar()

        #------ constants for controlling layout and look  ------
        self.button_width         = 6

        self.button_padx          = "2m"
        self.button_pady          = "1m"

        self.btn_color            = self.parameters.btn_color
        self.bkg_color            = self.parameters.bkg_color

        next_frame       = 0      # index of frames and position row for frames

#        self.root_b      = Frame( self.root )   # this may be an extra unneeded frame
        self.root_b      =  self.root # !! to phase out root_b -- run a bit more the finish delete of _b
        #self.root.grid( column=1, row=1 )  # this seems to set up the col grid in the root
        #self.root.pack( expand = True, sticky = E+W )  # this also works, why needed? sticky not an option here

        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
#        self.root.grid_rowconfigure(    0, weight=1 )

        a_frame  = self._make_query_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame  = self._make_device_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame  = self._make_db_frame( self.root_b,  )
        a_frame.grid( row=next_frame, column=0, sticky = E + W + N + S )   # + N + S  )  # actually only expands horiz
        next_frame += 1

        a_frame = self._make_button_frame( self.root_b,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N)
        next_frame += 1

        a_frame = self._make_message_frame( self.root_b,  )
        a_frame.grid(row=next_frame, column=0, sticky=E + W + N + S)
        next_frame += 1

        self.root_b.grid_columnconfigure( 0, weight=1 )
        self.root_b.grid_rowconfigure(    0, weight=0 )
        self.root_b.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

#        #        # -------- does this help
#        self.root.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

    #------ build frames  ------------------------
        # ------------------------------------------
    def _make_device_frame( self, parent, ):
        """
        device frame, list devices
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg =self.bkg_color, relief=RAISED, borderwidth=1 )

        rowspan    = 2

        for ix, i__smartplug in enumerate(  AppGlobal.smartplug_adapter_list ) :
            lcol      = 0
            lrow      = ix
            #a_widget  = Button( a_frame , width=10, height=2, text = i__smartplug_dict[ "name" ] )

            cb_var   = IntVar() # how to get

            a_widget = Checkbutton( a_frame, text = i__smartplug.name,  variable = cb_var, ) # add later command=cb_cb )

            i__smartplug.gui_tk_checkbox        = a_widget  # maybe drop not sure if used
            i__smartplug.gui_tk_checkbox_var    = cb_var

            #callback=lambda x=x: f(x)
            # a_button.device_id =..... but still eval a_button later
            #a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "info" ) )
            a_widget.grid( row = lrow * rowspan, column = 0, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

        return a_frame

    # ------------------------------------------
    def _make_db_frame( self, parent, ):
        """
        make a frame for db connect and .....
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg =self.bkg_color, relief=RAISED, borderwidth=1 )

        # add some more for db, different style, which do I like best?
        lrow   =  0
        lcol   =  0
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        bw_for_db      = FileBrowseWidget( a_frame )
        bw_for_db.grid( row = lrow, column = lcol )
        bw_for_db.set_text( AppGlobal.parameters.db_file_name )
        self.bw_for_db = bw_for_db  # save reference

        return  a_frame

    # ------------------------------------------
    def _make_query_frame( self, parent, ):
        """
        make parameter frame for queries

        Return: a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg = self.bkg_color, relief=RAISED, borderwidth=1 )

        # add some more for db, different style, which do I like best?
        lrow   =  0
        lcol   =  0

        # some spacers might be nice -- may put back as we play with the look
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )

        # ------------------------------------
        # !! do not need to save lables
        lrow    += 1
        ( lrow, lcol, self.lbl_start )   = self._make_label( a_frame, lrow, lcol, "Start date and hour:", )
        ( lrow, lcol, self.lbl_end   )   = self._make_label( a_frame, lrow, lcol, "End date and hour:", )
        #( lrow, lcol, self.lbl_db_user )   = self._make_label( a_frame, lrow, lcol, "user", )

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
        self.cal_end     = cal  # save for later

        #-------------------------------------
        lrow    = 0
        lcol    = 3

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
        a_widget.set( self.parameters.graph_begin_hr )
        self.time_begin  = a_widget

        a_widget   =  ttk.Combobox( a_frame, values=AppGlobal.dd_hours, state='readonly')
        a_widget.grid( row = lrow + 1, column = lcol, rowspan = 1, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
        a_widget.set( self.parameters.graph_end_hr )
        self.time_end  = a_widget

        #------------- some of this may be added back later or not ---------------

        lrow    = 0
        lcol    = 4
        a_rb   =  Radiobutton( a_frame, text = "From Parms   ",      variable = self.rb_var, value=0,  command = self.controller.cb_rb_select )
        a_rb.grid( row = lrow,  column = lcol )

        #lrow   = 1
        lcol   += 1
        a_rb   =  Radiobutton( a_frame, text = "Today",             variable = self.rb_var, value=1,  command=self.controller.cb_rb_select )
        a_rb.grid( row = lrow,  column = lcol )


        #lrow    = 0
        lcol    += 1
        a_rb   =  Radiobutton( a_frame, text = "From Now - 1hr ",      variable = self.rb_var, value=6,  command=self.controller.cb_rb_select )
        a_rb.grid( row = lrow,  column = lcol )

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

#        lrow    = 0
#        lcol    += 1
#        a_rb   =  Radiobutton( a_frame, text = "From Now - 1hr ",      variable = self.rb_var, value=6,  command=self.controller.cb_rb_select )
#        a_rb.grid( row = lrow,  column = lcol )

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
#        ( lrow, lcol, self.lbl_db_connect )   = self._make_label( a_frame, lrow, lcol, "connect", )
#        ( lrow, lcol, self.lbl_db_host )      = self._make_label( a_frame, lrow, lcol, "host", )
#        ( lrow, lcol, self.lbl_db_db )        = self._make_label( a_frame, lrow, lcol, "db", )
#        ( lrow, lcol, self.lbl_db_user )      = self._make_label( a_frame, lrow, lcol, "user", )

        return  a_frame

    # ------------------------------------------
    def _make_label( self, a_frame, a_row, a_col, a_text, ):
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
    def _make_button_frame( self, parent, ):
            """
            make a test frame place for test stuff esp. buttons
            """
            a_frame  = Frame( parent, width=300, height=200, bg = self.parameters.id_color, relief=RAISED, borderwidth=1 )

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

            # about
            a_button = Button( a_frame , width=10, height=2, text = "About" )
            a_button.config( command = self.controller.cb_about )
            a_button.pack( side = LEFT )

            # restart
            a_button = Button( a_frame , width=10, height=2, text = "Restart" )
            a_button.config( command = self.controller.restart )
            a_button.pack( side = LEFT )

            a_button = Button( a_frame , width=10, height=2, text = "Test" )
            a_button.config( command = self.controller.cb_test )
            a_button.pack( side = LEFT )

            return a_frame

    # ------------------------------------------
    def _make_message_frame( self, parent,  ):
        """
        a frame with scrolling text area and controlls for it
        -- there is a scrolled_tet control, not currently using it --- why??
        """
        self.max_lines      = 500
        self.cb_scroll_var  = IntVar()  # for check box in reciev frame
        color   = "red"
        iframe  = Frame( parent, width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )

        bframe  = Frame( iframe, bg ="black", width=30  ) # width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )
        bframe.grid( row=0, column=0, sticky = N + S )

        text0 = Text( iframe , width=50, height=20 )
        #text0.configure( bg = "red" )
#        self.save_redir = RedirectText( text0 )

        s_text0 = Scrollbar( iframe  )  # LEFT left
        s_text0.grid( row=0, column=2, sticky = N + S )

        s_text0.config( command=text0.yview )
        text0.config( yscrollcommand=s_text0.set )

        text0.grid( row=0, column=1, sticky = N + S + E + W  )

        self.rec_text  = text0

        iframe.grid_columnconfigure( 1, weight=1 )
        iframe.grid_rowconfigure(    0, weight=1 )

        # spacer
        s_frame = Frame( bframe, bg ="green", height=20 ) # width=30  )
        s_frame.grid( row=0, column=0  )
        row_ix   = 0

        # --------------------
        b_clear = Button( bframe , width=10, height=2, text = "Clear" )
        b_clear.bind( "<Button-1>", self.do_clear_button )
        b_clear.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_temp = Button( bframe , width=10, height=2, text = "for_what"
                        )
        b_temp.bind( "<Button-1>", self.doButtonText )
        b_temp.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_copy = Button( bframe , width=10, height=2, text = "copy all" )
        b_copy.bind( "<Button-1>", self.do_copy_button )
        b_copy.grid( row=row_ix, column=0   )
        row_ix += 1

        # -------------
        a_widget = Checkbutton( bframe,  width=7, height=2, text="A Scroll", variable=self.cb_scroll_var,  command=self.do_auto_scroll )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        self.cb_scroll_var.set( self.parameters.default_scroll )

        return iframe
    # ------------------------------------------
    def get_checked_device_adapters( self ):
        """
        what it says
        return list (device_adapter..... ) or empty
        """
        device_adapter_list = []
        for i_device_adapter in AppGlobal.smartplug_adapter_list:
            # ?? list comp instead
#            print( f"{i_device_adapter.name} i_device_adapter.gui_tk_checkbox_var  {i_device_adapter.gui_tk_checkbox_var}")
            if i_device_adapter.gui_tk_checkbox_var.get():
                device_adapter_list.append( i_device_adapter )
#                print( f"checked devices: {i_device_adapter.name} ")
        return device_adapter_list

    # ------------------------------------------
    def get_begin_end( self ):
        """
        what it says:
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
        what it says
        its name, return a string
        """
        #bw_for_db.set_text     = AppGlobal.parameters.db_file_name
        # x = 1/0   # think should get directly from AppGlobal
        return( self.bw_for_db.get_text() )

    # ------------------------------------------
    def display_info_string( self, data, update_now = False ):
        """
        add info prefix and new line suffix and show in recieve area
        data expected to be a string, but other stuff has str applied to it
        consider adding auto log
        """
        tab_char   = "\n"
        sdata      = f">>{data}{tab_char}"
        self.display_string( sdata, update_now = update_now )
        return

    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
        """
        print to recieve area, with scrolling and
        delete if there are too many lines in the area
        logging here !!
        """
        if  AppGlobal.parameters.log_gui_text:
            AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )
             #AppGlobal.logger.info( a_string )     # not sure about this level

        self.rec_text.insert( END, a_string, )      # this is going wrong, why how
        try:
             numlines = int( self.rec_text.index( 'end - 1 line' ).split('.')[0] )  # !! beware int( None ) how could it happen ?? it did this is new
        except Exception as exception:
        # Catch the custom exception
            self.logger.error( str( exception ) )
            print( exception )
            numlines = 0
        if numlines > self.max_lines:
            cut  = int( numlines/2  )   # lines to keep/remove py3 new make int
            # remove excess text
            self.rec_text.delete( 1.0, str( cut ) + ".0" )
            #msg     = "Delete from test area at " + str( cut )
            #self.logger.info( msg )

        if self.cb_scroll_var.get():
            self.rec_text.see( END )

        if update_now:
            self.root.update()
        return

    # ----- button actions - this may be to indirect for some actions that go to the controller  ------------------------
    # ------------------------------------------
    def do_restart_button( self, event):
        self.controller.restart()
        return

#    # ------------------------------------------
#    def do_open_button( self, event):
#        self.controller.open_com_driver()
#        return

    # ------------------------------------------
    def do_clear_button( self, event):
        """
        for the clear button
        clear the recieve area
        """
        self.rec_text.delete( 1.0, END )
        return

    # ------------------------------------------
    def do_copy_button( self, event ):
        """
        copy all text to the clipboard
        """
        data  = self.rec_text.get( 1.0, END )
        pyperclip.copy( data )
        return

    # ------------------------------------------
    def do_graph( self,  ):
        """
        do the graph -- call should probably have been direct
        """
        self.controller.cb_graph()
        return

    # ------------------------------------------
    def do_auto_scroll( self,  ):
        """
        pass, not needed, place holder  -- may want to add back
        """
        # print "do_auto_scroll"
        # not going to involve controller
        pass
        return

    # ------------------------------------------
    def cb_send_button( self, event ) :  # how do we identify the button    def cb_send_button( self, event ) :  # how do we identify the button
        """
        any send button
        for at least now do the send echo locally ( and crlf or always use locally )
        """
        #identify the control, one of send buttons, get text and send
        control_ix = -1
        for index, i_widget in enumerate( self.sends_buttons ):

            if i_widget == event.widget:
                control_ix = index
                break
        contents = self.sends_data[control_ix].get()

        self.controller.send( contents )
        return

    # --------------- may be left over from terminal check and delete dead stuff !!---------------------------
    def doButtonText( self, event):
        """
        easy to add functions that look at the button text
        but long term do not use
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
    let user pick a file name on their computer
    not sure why making it ino a widget is a good idea but here goes
    this is a widget that both holds a filename
    and lets you browse to a file
    how is it different from just a couple of widgets
    in your frame ... more reusable ?
    better looking or what
    see graph_smart_plug gui for a use
    !! code is duplicated in 2 guis, this should be fixed
    right now linking to app global, this is really bad, should have a way to control at runtime
    """
    def __init__(self, parent ):
        #super( BrowseWidget, self ).__init__( parent, width=60, height=20, bg ="red")
        super(  ).__init__( parent, width=60, height=20, bg ="red")
        self.label_1      = Label( self, text="Database File: ").grid(row=1, column=0)

        self.a_string_var = StringVar()

        self.entry_1      = Entry( self , width=100,   text = "bound", textvariable = self.a_string_var )
        self.entry_1.grid( row=1, column=1 )

        self.button_2 = Button( self, text="Browse...", command = self.browse )
        self.button_2.grid( row=1, column=3 )

    # ------------------------------------------
    def browse( self ):
        """
        browse for a file name
        return full path or "" if no file chosen

        from tkinter import filedialog
        from tkinter import *

        root = Tk()
        root.filename =  filedialog.askopenfilename( initialdir = "/",
                                            title = "Select file",
                                            filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        print (root.filename)
        or use asksaveasfilename
        filedialog.asksaveasfile
        import tkinter.filedialog
        !! have not found docs ... do an ex_ file
        tkinter.filedialog.asksaveasfilename()
        tkinter.filedialog.asksaveasfile()
        tkinter.filedialog.askopenfilename()
        tkinter.filedialog.askopenfile()
        tkinter.filedialog.askdirectory()
        tkinter.filedialog.askopenfilenames()
        tkinter.filedialog.askopenfiles()


        """
        Tk().withdraw()
        #self.root.withdraw() # not part of gui so out of scope !! would it be better to get a gui reference
#        filename     = asksaveasfile(  initialdir   = "./",
#                                         title        = "Select file for db",
#                                         filetypes    = (("database files","*.db"),("all files","*.*")))

        filename     = askopenfilename(  initialdir   = "./",
                                         title        = "Select file for db",
                                         filetypes    = (("database files","*.db"),("all files","*.*")))
        if filename == "":
            return

        self.set_text( filename )
        print( f"get_text = {self.get_text()}", flush = True )
#        bad idea AppGlobal.db_file_name   = filename

    # ------------------------------------------
    def set_text( self, a_string ):
        """
        get the text from the entry
        """
        self.a_string_var.set( a_string )

    # ------------------------------------------
    def get_text( self, ):
        """
        get the text from the entry -- this is how to get db name at all times
        """
        a_string   =  self.a_string_var.get(  )
        return( a_string )

# =======================================

# import test_controller # no longer used

if __name__ == '__main__':
        """
        run the app
        """
        import  smart_plug_graph
        a_app = smart_plug_graph.SmartPlugGraph(  )


