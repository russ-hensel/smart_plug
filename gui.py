# -*- coding: utf-8 -*-
#
"""
 gui    for smartplug

"""


import  logging
import  pyperclip
from    tkinter import *   # is added everywhere since a gui assume tkinter namespace
import  sys
from    tkinter import ttk

# local imports
from app_global import AppGlobal


class RedirectText(object):
    """
    not currently used ???
    simple class to let us redirect console prints to our recieve area
    http://www.blog.pythonlibrary.org/2014/07/14/tkinter-redirecting-stdout-stderr/

    """
    #----------------------------------------------------------------------
    def __init__(self, text_ctrl):
        """
        text_ctrl text area where we want output to go
        """
        self.output = text_ctrl

    #----------------------------------------------------------------------
    def write(self, string):
        """
        """
        self.output.insert( END, string )
        # add scrolling?
        self.output.see( END )

        #self.rec_text.insert( END, adata, )
        #self.rec_text.see( END )

    #--------------------------------
    def flush(self, ):
        """
        here to mimic the standard sysout
        does not really do the flush
        """
        pass

# ======================= begin class ====================

class GUI( object ):
    """
    gui for the application
    you should be able to make replacements without messing with
    much code in other places than your replacement GUI
    """
    def __init__( self, ):

        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters
        AppGlobal.gui           = self
        self.gui_running        = False
        self.root               = Tk()    # this is the tkinter root for the GUI move to gui after new working well plus bunch after here

        a_title   = self.controller.app_name + " version: " + self.controller.version # + " mode: " + self.parameters.mode
        self.root.title( a_title )
        self.root.geometry( self.parameters.win_geometry )

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")
        #self.logger.info( "in class gui.GUI init")

        self.save_redir          = None

        self.save_sys_stdout     = sys.stdout   # think obsolete

        self.rec_text            = None    # set later   # ?? rename globally later

        self.show_dict           =  {}    # populate as fileds are built  ?? old idea?

        self.max_lines           = self.parameters.max_lines    # max lines in recieve area then delete fraction 1/2 now

        self.prefix_info         = self.parameters.prefix_info

        #Button names -- this is a method I am not sure I will use in the future

        self.BN_CP_SELECTION      = "Copy Sel"
        self.BN_CVERT             = "Cvert"
        self.BN_CP_ALL            = "Copy All"

        #------ END constants for controlling layout ------

        # --------- gui standards work on more have themes have in another object ?
        # but there are things called themes, look for more docu
        self.btn_color     = self.parameters.btn_color
        self.bkg_color     = self.parameters.bkg_color
        #self.text_color    = "white"

        next_frame = 0    # position row for frames

        self.root.configure(background = self.bkg_color )

        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
#        self.root.grid_rowconfigure(    0, weight=1 )

        a_frame = self._make_button_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky = E + W + N )
        next_frame += 1

        a_frame = self._make_smart_plug_frame( self.root,  )
        a_frame.grid( row = next_frame, column=0, sticky = E + W + N)
        next_frame += 1

        # ------------ message frame ---------------------
        self.cb_scroll_var  = IntVar()  # for check box in reciev frame

        a_frame    = self._make_message_frame( self.root,   )
        self.rec_frame    = a_frame
        a_frame.grid( row=next_frame, column=0, sticky= E + W + N + S )
        next_frame += 1

#        # -------- does this help
        self.root.grid_rowconfigure( ( next_frame - 1 ), weight=1 )

    #------ build frame methods ------------------------
    # ------------------------------------------
    def _make_id_frame( self, parent, ):
        """
        make a frame to help ID the app, initially a color band.
        not implemented ?? but may be nice to have
        """
        a_frame  = Frame( parent, width=300, height=20, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )

        return a_frame

#    # ------------------------------------------
#    def _make_parm_frame( self, parent, ):
#        """
#        make parameter frame
#        open/close port show port parms
#        arg: parent is parent widget
#        return frame to be placed
#        """
#        a_frame  = Frame( parent, width=600, height=200, bg =  self.parameters.bk_color, relief=RAISED, borderwidth=1 )
#
#        lrow   =  0
#        lcol   =  0
#        a_spacer  = Frame( a_frame, width=60, height=60, bg =self.parameters.id_color, relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column=1, sticky=E + W + N + S, rowspan = 2 )
#
#        lrow   =  0
#        lcol   += 1
#        a_label   = ( Label( a_frame, text = "Communications >>", relief = RAISED,  )  )
#        a_label.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#
#        # ---------
#        for ix in range( self.max_lables ):
#            self.lables.append( Label( a_frame, text = "lbls" + str( ix ), relief = RAISED,  )  )
#
#        lrow    = 0
#        lcol   += 2
#        #lcol   += 1
#        for i_label in self.lables:
#            #print "label at ", lrow, lcol
#            i_label.grid( row=lrow, column=lcol, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#
#            lrow    += 1
#            if lrow >= 2:
#                lrow   =  0
#                lcol   += 1
#
#        for ix in range(  2, lcol  ):
#            a_frame.grid_columnconfigure( ix, weight=0 )
#
#        # add some more for db, different style, which do I like best?   self.parameters.bk_color
#        lrow   =  0
#        lcol   += 1
#        a_spacer  = Frame( a_frame, width=60, height=60, bg = self.parameters.bk_color, relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )
#
#        lrow   =  0
#        lcol   += 1
#        a_label   = ( Label( a_frame, text = "Database >>", relief = RAISED,  )  )
#        a_label.grid( row = lrow, column = lcol, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#
#        lcol   += 1
#        #lrow    += 1
#        if lrow >= 2:
#            lrow   =  0
#            lcol   += 1
#
#        a_label   = ( Label( a_frame, text = "status", relief = RAISED,  )  )
#        a_label.grid( row=lrow, column=lcol, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#        self.lbl_db_status                    = a_label
#        self.show_dict[ 'db_status' ]         = a_label
#
#        ( lrow, lcol, self.lbl_db_connect )   = self._make_a_label( a_frame, lrow, lcol, "connnect", )
#        self.show_dict[ 'db_connect' ]        = self.lbl_db_connect      # Add new entry
#
#        ( lrow, lcol, self.lbl_db_host )      = self._make_a_label( a_frame, lrow, lcol, "host", )
#        self.show_dict[ 'db_host' ]           = self.lbl_db_host
#
#        ( lrow, lcol, self.lbl_db_db )        = self._make_a_label( a_frame, lrow, lcol, "db", )
#        self.show_dict[ "db_db" ]             = self.lbl_db_db
#
#        ( lrow, lcol, self.lbl_db_user )      = self._make_a_label( a_frame, lrow, lcol, "user", )
#        self.show_dict[ "db_user" ]           = self.lbl_db_user
#
#        #( lrow, lcol, a_lbl        )          = self._make_a_label( a_frame, lrow, lcol, "Extraaaa", "extra", self.show_dict )
#        #self.show_dict[ "Extra" ]           = a_lbl
#
#        return  a_frame

#     # ------------------------------------------
#    def _make_helper_frame( self, parent, ):
#        """
#        make helper frame place to display helper info/status
#        this may be only for debugging
#        arg: parent is parent widget
#        return frame to be placed
#        """
#        a_frame  = Frame( parent, width=600, height=20, bg ="gray", relief=RAISED, borderwidth=1 )
#
#        lrow   =  0
#        lcol   =  0
#        a_label   = Label( a_frame, text = "auto", relief = RAISED, width = 100, ) # wraplength = 90   )
#        a_label.grid( row = lrow, column = lcol, columnspan=10,  sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#
#        self.show_dict[ "helper_info" ]   =  a_label    # if not there then  houston we have a prblem
#        #self.helper_label     = a_label   # only helper writes to it
#
#        return  a_frame

    # ------------------------------------------
#    def make_cc_button_frame( self, parent, ):
    def _make_button_frame( self, parent, ):
        """
        this is the primary frame for the standard gui buttons pretty much for all modes
        """
        a_frame  = Frame( parent, width=300, height=200,
                         #bg          = self.parameters.id_color,
                         bg          = self.parameters.bkg_color,
                         relief      = RAISED, borderwidth=1 )

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

        a_button = Button( a_frame , width=10, height=2, text = "Restart" )
        a_button.config( command = self.controller.restart )
        a_button.pack( side = LEFT )

#       keeep for a test button
        a_button = Button( a_frame , width=10, height=2, text = "Test" )
        #a_button.config( command = self.controller.cb_test )
        a_button.config( command = self.cb_test_1 )
        a_button.pack( side = LEFT )

        a_button = Button( a_frame , width=10, height=2, text = "Help" )
        a_button.config( command = self.controller.os_open_helpfile )
        a_button.pack( side = LEFT )

        return a_frame

        # ------------------------------------------
    def _make_smart_plug_frame( self, parent, ):
        """
        one button set for each smartplug, config from parameters
        consider column titles ??
        note cute lambda
        may want to put function call in the array ... no ??
        """
        a_frame  = Frame( parent, width=300, height=200,
                         bg          = self.bkg_color,
                         relief      = RAISED, borderwidth=1 )

        rowspan    = 2

        for ix__smartplug_adapter, i_smartplug_adapter in enumerate( self.controller.smartplug_adapter_list ):
            lcol      = 0
            lrow      = ix__smartplug_adapter
            a_button  = Button( a_frame , width=10, height=2, text = i_smartplug_adapter.name )
            #callback=lambda x=x: f(x)
            # a_button.device_id =..... but still eval a_button later
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "info" ) )
            a_button.grid( row = lrow * rowspan, column = 0, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "On"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "on" ) )
            a_button.grid( row = lrow * rowspan, column = 1, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "Off"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "off" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "Record On"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "record_on" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "Record Off"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "record_off" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "Retrieve"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "retrieve" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            a_button  = Button( a_frame , width=10, height=2, text = "Start Timer for:"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "start" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            #print( "made device button" )
            lcol +=  1

            times = ( "infinite", .1, .5, 1,  2, 3, 5, 10, 15, 20, 25, 30, 40, 50, 60  )   # think about adding units...
            #cbp3 = ttk.Labelframe(demoPanel, text='Pre-defined List')  # see ex_tkcombobox
            a_widget   =  ttk.Combobox( a_frame, values=times, state='readonly', ) # text = "infinite" ) does not work
            a_widget.current( 6 )    # set vaue
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )
            i_smartplug_adapter.gui_tk_combo = a_widget
            lcol +=  1

            # once lable width set seems to stick -- adjust to your liking
            a_widget   =  Label( a_frame, text =  80*" ", justify = LEFT, anchor = W,
                                 borderwidth = 5, relief = RAISED,  )
            a_widget.config( width = 30)   # if not set adjusts to text

            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky = E + W + N + S )
            i_smartplug_adapter.gui_tk_label  = a_widget
            lcol +=  1

        return a_frame

    # ------------------------------------------
    def _make_one_send_frame( self, parent, ix_send ):
        """
        make a new send frame, for just one button and text entry to send
        return frame for placement
        """
        # print "___make_send_frame__"  color does not really work here as sends fill area
        send_frame  = Frame( parent, width=300, height=200, bg=self.parameters.id_color, relief=RAISED, borderwidth=1 )

        a_text = Entry( send_frame , ) # width=50, ) # height=2 )
        a_text.configure( bg = "gray" )
        a_text.delete(0, END)    # this may be bad syntax when use eleswher

        if ix_send < len( self.parameters.send_strs ):
            send_str  = self.parameters.send_strs[ ix_send ]
        else:
            send_str  = ""

        a_text.insert( 0, send_str )

        a_button = Button( send_frame , width=10, height=2, text = "Send" )
        a_button.bind( "<Button-1>", self.cb_send_button ) # function name no () which would call function then

        # position
        a_button.pack( side = LEFT )
        a_text.pack(  side = LEFT, fill=BOTH, expand=1)  #  fill X Y BOTH but also need expand=1 ( or prehaps True )

        # save for send function
        self.sends.append( send_frame )
        self.sends_buttons.append( a_button )
        self.sends_data.append( a_text )

        return send_frame

#    # ------------------------------------------
#    def _make_send_frame( self, parent,  ):  # if this were a class then could access its variables later
#        """
#        make a new send frame containing little send frames
#        """
#        # print "___make_send_frame__"  color does not really work here as sends fill area
#
#        send_frame        = Frame( parent, width=300, height=200,
#                                    #bg = self.parameters.bk_color,
#                                    bg = "green",
#                                    relief=RAISED, borderwidth=1 )
#        self.ix_send      = 0
#        self.send_frames  = []
#        ix_row            = 0
#        ix_col            = 0
#
#        # convert the parameter send_ctrls to our tuple form to make later processing easier
#        ix_max_row        = self.parameters.max_send_rows
#        parm_send_ctrls   = self.parameters.send_ctrls
#        send_ctrls        = []
#
#        for ix in range( self.parameters.gui_sends ):
#
#            if ix < len( parm_send_ctrls ):
#                parm_send_ctrl  = parm_send_ctrls[ ix ]
#                if type( parm_send_ctrl ).__name__ == "tuple":
#                    #print "is tuple"
#                    send_ctrl  = parm_send_ctrl
#                else:
#                    # then it is text
#                    send_ctrl  = ( "Send", parm_send_ctrl, True )
#            else:
#                send_ctrl  = ( "Send", "", True )
#            #print( send_ctrl )
#            send_ctrls.append( send_ctrl )
#        #print( send_ctrls )
#
#        for i_send_ctrl  in send_ctrls:
#
#            send_frame1    =  self._make_one_send_frame_new( send_frame, self.ix_send, i_send_ctrl   )
#            self.send_frames.append( send_frame1 )
#            send_frame1.grid( row=ix_row,  column=ix_col, sticky= E + W + N  )
#
#            self.ix_send   += 1
#            ix_row         += 1
#            if ix_row >= ix_max_row:
#                ix_row    = 0
#                ix_col    += 1
#
#        return send_frame
#
#    # ------------------------------------------
#    def _make_one_send_frame_new( self, parent, ix_send, ctrl_info ):  # if this were a class then could access its variables later
#        """
#        make a new send frame, for just one button and text entry to send
#        """
#        ( b_text, s_text, s_enable )  = ctrl_info
#
#        # print "___make_send_frame__"  color does not really work here as sends fill area
#        #send_frame  = Frame( parent, width=300, height=200, bg=self.parameters.bk_color, relief=RAISED, borderwidth=1 )  # maybe color should always be gray
#        send_frame  = Frame( parent, width=300, height=200, bg="gray", relief=RAISED, borderwidth=1 )  # maybe color should always be gray
#
#        a_text = Entry( send_frame , ) # width=50, ) # height=2 )
#        a_text.configure( bg = "gray" )
#        a_text.delete(0, END)    # this may be bad syntax when use eleswher
#
#        a_text.insert( 0, s_text )
#
#        if s_enable:
#            a_text.config( state =  NORMAL   )
#        else:
#            a_text.config( state =  DISABLED )
#
#        a_button = Button( send_frame , width=10, height=2, text = b_text )
#        a_button.bind( "<Button-1>", self.cb_send_button ) # function name no () which would call function then
#
#        # position
#        a_button.pack( side = LEFT )
#        a_text.pack(   side = LEFT, fill=BOTH, expand=1)  #  fill X Y BOTH but also need expand=1 ( or prehaps True )
#
#        # save for send function
#        self.sends.append( send_frame )
#        self.sends_buttons.append( a_button )
#        self.sends_data.append( a_text )
#
#        return send_frame

    # ------------------------------------------
    def _make_message_frame( self, parent,  ):
        """
        make the message frame
        """
#        color   = "black"   # this may need a bit of rework -- looks like not used
        iframe  = Frame( parent, width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )

        bframe  = Frame( iframe, bg = self.bkg_color, width=30  ) # width=300, height=800, bg ="blue", relief=RAISED, borderwidth=1,  )
        bframe.grid( row=0, column=0, sticky = N + S )

        text0 = Text( iframe , width=50, height=20 )
        #text0.configure( bg = "red" )
        self.save_redir = RedirectText( text0 )

        s_text0 = Scrollbar( iframe  )  # LEFT left
        s_text0.grid( row=0, column=2, sticky = N + S )

        s_text0.config( command=text0.yview )
        text0.config( yscrollcommand=s_text0.set )

        text0.grid( row=0, column=1, sticky = N + S + E + W  )

        self.rec_text  = text0

        iframe.grid_columnconfigure( 1, weight=1 )
        iframe.grid_rowconfigure(    0, weight=1 )

        # now into the button frame bframe

        # spacer
        s_frame = Frame( bframe, bg ="green", height=20 ) # width=30  )
        s_frame.grid( row=0, column=0  )
        row_ix   = 0

        # --------------------
        b_clear = Button( bframe , width=10, height=2, text = "Clear" )
        b_clear.bind( "<Button-1>", self.doClearButton )
        b_clear.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_temp = Button( bframe , width=10, height=2, text = self.BN_CP_SELECTION )
        b_temp.bind( "<Button-1>", self.doButtonText )
        b_temp.grid( row=row_ix, column=0   )
        row_ix   += 1

        #-----
        b_copy = Button( bframe , width=10, height=2, text = self.BN_CP_ALL )
        b_copy.bind( "<Button-1>", self.do_copy_button )
        b_copy.grid( row=row_ix, column=0   )
        row_ix += 1

        # -------------
        a_widget = Checkbutton( bframe,  width=7, height=2, text="A Scroll", variable=self.cb_scroll_var,  command=self.do_auto_scroll )
        a_widget.grid( row=row_ix, column=0   )
        row_ix += 1

        self.cb_scroll_var.set( self.parameters.default_scroll )

        return iframe

#    # ------------------------------------------
#    def _make_a_label( self, a_frame, a_row, a_col, a_text, label_id = None, label_dict = None ):
#        """
#        a_id   id for lable in the dict
#        a_dict will contain the label reference now used for setting text as in show_item
#        helper for making and placing labels
#        return tuple -- or by ref do not need to , test this in templates
#        return label
#        increment row col
#        """
#        a_row    += 1
#        if a_row >= 2:
#            a_row   =  0
#            a_col   += 1
#
#        a_label   = ( Label( a_frame, text = a_text, relief = RAISED,  )  )
#        a_label.grid( row=a_row, column=a_col, sticky = E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#
#        if not( label_id is None ):
#            label_dict[ label_id ]   =  a_label
#
#        return ( a_row, a_col, a_label )

    #-----  functions mostly for calling from controller  ------------------------
    # ------------------------------------------
    def run( self,  ):
        """
        run the gui
        will block untill destroped, except for polling method in controller
        """
        # move from controller to decouple type of gui
        self.gui_running        = True
#        self.root.after( self.parameters.gt_delta_t, self.controller.polling )
        self.root.mainloop()
        self.gui_running        = False

    # ------------------------------------------
    def close( self, ):
        if self.gui_running:
             self.root.destroy()
        else:
            pass

    # ------------------------------------------
    def show_item( self, item_name, a_show_string ):
        """
        display a message on the gui -- mostly db info for mysql not used in this app.

        arg:  item_name, string name for the label widget, assigned to the dict when label is constructed
              a_show_string, the string you want shown
        notes:
              if the item_name is not found log an error, not exception
              this will work for any label in the dictionary else except for if caluse below log a message
        """
        lbl    =  self.show_dict.get( item_name, None )

        if lbl is None:
            if item_name == "helper_info":
                pass
            else:
            # error, but system should go on, for helper info we should suppress, just means helper not created  if item_name =
                msg   = "show_item, item = " + item_name + " not in dict to show: " + a_show_string
                self.logger.error( msg )
        else:
            lbl.config(  text    =  a_show_string )

    # ------------------------------------------
    def print_send_string( self, data ):
        """
        obsolete fix name !!
        add recieve tag to parameters ??
        """
        sdata = self.prefix_send + data  + "\n"
        self.display_string( sdata )   # or just use directly
        return

    # ------------------------------------------
    def print_rec_string( self, data ):
        """
        obsolete
        """
        sdata = self.prefix_rec +  data  + "\n"
        self.display_string( sdata )
        return

    # ------------------------------------------
    def print_info_string( self, data ):
        """
        add info prefix and new line suffix and show in recieve area
        """
        sdata = self.prefix_info +  data  + "\n"    # how did data get to be an int and cause error ??
        self.display_string( sdata )
        return

    # ------------------------------------------
    def print_no_pefix_string( self, data ):
        """
        add new line suffix and show in recieve area
        """
        sdata = data  + "\n"
        self.display_string( sdata )
        return

    # ---------------------------------------
    def display_string( self, a_string ):
        """
        print to message area, with scrolling and
        log if we are configured for it
        delete if there are too many lines in the area
        """
        if  AppGlobal.parameters.log_gui_text:
            AppGlobal.logger.log( AppGlobal.parameters.log_gui_text_level, a_string, )

        self.rec_text.insert( END, a_string, )      # this is going wrong, why how
        try:
             numlines = int( self.rec_text.index( 'end - 1 line' ).split('.')[0] )  # !! beware int( None ) how could it happen ?? it did this is new
        except Exception as exception:
        # Catch the custom exception
            self.logger.error( str( exception ) )
            print( exception )
            numlines = 0
        if numlines > self.max_lines:
            cut  = numlines/2     # lines to keep/remove
            # remove excess text
            self.rec_text.delete( 1.0, str( cut ) + ".0" )
            #msg     = "Delete from test area at " + str( cut )
            #self.logger.info( msg )

        if self.cb_scroll_var.get():
            self.rec_text.see( END )

        return

#    # ------------------------------------------
#    def display_device_label( self, msg, device_adapter  ):
#        """
#        not needed ?? done by actions directly in device adapter
#        display msg in the device's label area
#        """
#        label       = device_adapter.gui_tk_label
#        label.config( text = msg )

    #----- buttons ------------------------
    # ------------------------------------------
    def cb_device_action( self, button_ix, action  ):
        """
        process devices perhaps on, off timer , see lambda setup in button creation
        this may be more indirect than needed, go straight to controller ??
        """
#        print( f"cb_device_action {button_ix}, {action}" )

        self.controller.cb_device_action( button_ix, action  )

    # ------------------------------------------
    def cb_test_1( self ):
        """
        process test button 1
        """
        print( "cb_test_1" )
        self.controller.cb_gui_test_1()

    # ------------------------------------------
    def doButtonText( self, event):
        """
        easy to add functions that look at the button text
        """
        btext =  event.widget["text"]

        if btext == self.BN_CP_SELECTION:
            #def do_copy_button( self, event ):
            # nogood if no selection put in try except
            try:
                data  = self.rec_text.get( "sel.first", "sel.last" )
                pyperclip.copy( data )
            except Exception as exception:  # if no selection
                pass

            return

        elif btext == "Copy All":

            # may be in do CopyButton
            #def do_copy_button( self, event ):
            """
            """
            data  = self.rec_text.get( 1.0, END )
            pyperclip.copy( data )
            return

        elif btext == "Cvert":
            # print btext
            adata   =  self.rec_text.get( 1.0, END )

            #bdata  = dataConvert1( adata )
            #self.text1.delete( 1.0, END )
            #adata = "this is the text called adata that is..... "
            #self.text1.insert( END, bdata, )
            #self.text1.see( END )

            data_splits   = adata.split( " " )

            cdata  = []
            for item in data_splits:

                try:
                    value = int( item )
                    item  = str( value/50 )  # needs to go back to string for join

                except ValueError:
                    pass
                cdata.append( item )

            sep = "\n"
            bdata   = sep.join( cdata )

            pyperclip.copy( bdata )
            self.rec_text.delete( 1.0, END )



        #        elif btext == self.BN_SND_ARRAY:
        #            #self.text0.delete( 1.0, END )
        #            #print btext
        #            self.controller.sendArray()
        #            pass

        # for screwing around
        elif btext == "Add DB":
            self.controller.addDB()
            pass

        elif btext == "Graph":
            self.controller.graph()
            pass

        else:
            msg   = "no action defined for: " + btext
            self.logger.error( msg )
        return

    # ------------------------------------------
    def doClearButton( self, event):
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
    def do_auto_scroll( self,  ):
        """
        pass, not needed, place holder
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

        # ---------------  end of button actions
# =======================================

if __name__ == '__main__':
    """
    run the app -- this may be old code, check that it is right against main app
    """
    import smart_plug
    a_app = smart_plug.SmartPlug(  )


