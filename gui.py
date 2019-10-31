# -*- coding: utf-8 -*-
#
"""
Purpose:
    gui    for smartplug

"""

import  logging
import  pyperclip
from    tkinter import *   # is added everywhere since a gui assume tkinter name space
from    tkinter.filedialog import askopenfilename
import  sys
from    tkinter import ttk
import  ctypes

# ------ local imports
from app_global import AppGlobal



# ======================= begin class ====================

class GUI( object ):
    """
    gui for the application
    you should be able to make replacements without messing with
    much code in other places than your replacement GUI
    """
    def __init__( self, ):
        AppGlobal.gui           = self
        self.controller         = AppGlobal.controller
        self.parameters         = AppGlobal.parameters

        self.gui_running        = False
        self.root               = Tk()
        a_title   = self.controller.app_name + " version: " + self.controller.version + " Mode: " +self.parameters.mode

        self.root.title( a_title )
        self.root.geometry( self.parameters.win_geometry )

        #        print( "next set icon " + str( self.parameters.os_win ) )
        if self.parameters.os_win:
            # from qt - How to set application's taskbar icon in Windows 7 - Stack Overflow
            # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105

            icon = self.parameters.icon
            if not( icon is None ):
#                print( "set icon "  + str( icon ))
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon)
                self.root.iconbitmap( icon )
            else:
                print( "No icon for you!"  + str( icon ))

        self.logger             = logging.getLogger( self.controller.logger_id + ".gui")
#        self.logger.info( "in class gui.GUI init")

        self.rec_text            = None    # set later   # ?? rename globally later

        self.show_dict           =  {}    # populate as fields are built  ?? old idea?

        self.max_lines           = self.parameters.max_lines    # max lines in receive area then delete fraction 1/2 now
        self.prefix_info         = self.parameters.prefix_info

        #Button names -- this is a method I am not sure I will use in the future
        self.BN_CP_SELECTION      = "Copy Sel"
        self.BN_CVERT             = "Cvert"
        self.BN_CP_ALL            = "Copy All"

        #------ END constants for controlling layout ------

        # --------- gui standards work on more have themes have in another object ?
        # but there are things called themes, look for more doc
        self.btn_color     = self.parameters.btn_color
        self.bkg_color     = self.parameters.bkg_color
        #self.text_color    = "white"

        next_frame = 0    # position row for frames

        self.root.configure(background = self.bkg_color )

        self.root.grid_columnconfigure( 0, weight=1 ) # final missing bit of magic
        #  self.root.grid_rowconfigure(    0, weight=1 )

        a_frame = self._make_button_frame( self.root,  )
        a_frame.grid(row=next_frame, column=0, sticky = E + W + N )
        next_frame += 1

        a_frame = self._make_smart_plug_frame( self.root,  )
        a_frame.grid( row = next_frame, column=0, sticky = E + W + N)
        next_frame += 1

        a_frame = self._make_db_frame( self.root,  )
        a_frame.grid( row = next_frame, column=0, sticky = E + W + N)
        next_frame += 1

        # ------------ message frame ---------------------


        a_frame           = self._make_message_frame( self.root,   )
        # self.rec_frame    = a_frame
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

    # ------------------------------------------
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

        a_button = Button( a_frame , width=10, height=2, text = "Probe Plugs" )
        a_button.config( command = self.controller.cb_probe )
        a_button.pack( side = LEFT )

#        #  graph
#        a_button = Button( a_frame , width=10, height=2, text = "Graph" )
#        a_button.config( command = self.controller.cb_graph_live )
#        a_button.pack( side = LEFT )

        #  keeep for a test button
        a_button = Button( a_frame , width=10, height=2, text = "Test" )
        a_button.config( command = self.cb_test_1 )
        a_button.pack( side = LEFT )

#        #  keeep for a test button
#        a_button = Button( a_frame , width=10, height=2, text = "Test2" )
#        a_button.config( command = self.controller.cb_gui_test_2 )
#        a_button.pack( side = LEFT )

        a_button = Button( a_frame , width=10, height=2, text = "Help" )
        a_button.config( command = self.controller.os_open_helpfile )
        a_button.pack( side = LEFT )

        # about
        a_button = Button( a_frame , width=10, height=2, text = "About" )
        a_button.config( command = self.controller.cb_about )
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

        # one section for each plug
        for ix__smartplug_adapter, i_smartplug_adapter in enumerate( self.controller.smartplug_adapter_list ):
            lcol      = 0
            lrow      = ix__smartplug_adapter
            a_button  = Button( a_frame , width=10, height=2, text = i_smartplug_adapter.name )
            #callback=lambda x=x: f(x)
            # a_button.device_id =..... but still eval a_button later
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "info" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = 2, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            # on off checkbox
            cb_on_var    = IntVar()
            a_widget     = Checkbutton( a_frame, text="Plug On", variable=cb_on_var, width = 10, anchor="w" )
            a_widget.config( command = lambda ix = ix__smartplug_adapter: self.controller.cb_device_action( ix, "cb_on" ) )
            a_widget.config( borderwidth = 5, relief = RAISED,  )
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = 2, sticky=E + W + N + S )
            i_smartplug_adapter.gui_tk_on_checkbox_var   = cb_on_var
            # these work as with lables
#            a_widget.config( width = 80)
#            a_widget.config( text='Hello World!',   anchor="e" )    # anchor alligns text
            lcol +=  1

            # monitor checkbox
            cb_mon_var    = IntVar()
            a_widget     = Checkbutton( a_frame, text="Monitor", variable=cb_mon_var, width = 10, anchor="w" )
            a_widget.config( command = lambda ix = ix__smartplug_adapter: self.controller.cb_device_action( ix, "mon" ) )
            a_widget.config( borderwidth = 5, relief = RAISED,  )
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = 2, sticky=E + W + N + S )
            i_smartplug_adapter.gui_tk_mon_checkbox_var   = cb_mon_var
            lcol +=  1

            # record checkbox
            cb_record_var    = IntVar()
            a_widget     = Checkbutton( a_frame, text="Record", variable=cb_record_var, width = 10, anchor="w" )
            a_widget.config( command = lambda ix = ix__smartplug_adapter: self.controller.cb_device_action( ix, "record" ) )
            a_widget.config( borderwidth = 5, relief = RAISED,  )
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = 2, sticky=E + W + N + S )
            i_smartplug_adapter.gui_tk_record_checkbox_var   = cb_record_var
            lcol +=  1

#            a_button  = Button( a_frame , width=10, height=2, text = "Retrieve"  )
#            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "retrieve" ) )
#            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
#            lcol +=  1

            a_button  = Button( a_frame , width=12, height=2, text = "Start Timer for:"  )
            a_button.config( command = lambda ix = ix__smartplug_adapter: self.cb_device_action( ix, "start" ) )
            a_button.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )    # sticky=W+E+N+S  )   # relief = RAISED)
            lcol +=  1

            # time combo box
            times = ( "infinite", ".1 min", ".5 min", "1 min",  "2 min", "3 min", "5 min", "10 min", "15 min",
                                  "20 min", "25 min", "30 min", "40 min", "50 min", "60 min"   )
            #cbp3 = ttk.Labelframe(demoPanel, text='Pre-defined List')  # see ex_tkcombobox
            a_widget   =  ttk.Combobox( a_frame, values=times, state='readonly',  width = 10, ) # text = "infinite" ) does not work
            a_widget.current( 3 )    # set default value
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky=E + W + N + S )
            i_smartplug_adapter.gui_tk_combo = a_widget
            lcol +=  1

            # output label widget
            # once Label width is set seems to stick -- adjust to your liking
            a_widget   =  Label( a_frame, text =  80*" ", justify = LEFT, anchor = W,
                                 borderwidth = 5, relief = RAISED,  )
            a_widget.config( width = 30)   # if not set adjusts to text

            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky = E + W + N + S )
            i_smartplug_adapter.gui_tk_label  = a_widget
            lcol +=  1

            # output label widget
            a_widget   =  Label( a_frame, text =  80*" ", justify = LEFT, anchor = W,
                                 borderwidth = 5, relief = RAISED,  )
            a_widget.config( width = 30)
            a_widget.grid( row = lrow * rowspan, column = lcol, rowspan = rowspan, sticky = E + W + N + S )
            i_smartplug_adapter.gui_tk_label_2  = a_widget
            lcol +=  1

        return a_frame

    # ------------------------------------------
    def _make_one_send_frame( self, parent, ix_send ):
        """
        make a new send frame, for just one button and text entry to send
        return frame for placement
        """
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

    # ------------------------------------------
    def _make_db_frame( self, parent, ):
        """
        make a frame for db connect and graphing, csv .....
        Return:  a frame with the controls in it
        """
        a_frame  = Frame( parent, width=600, height=200, bg =self.bkg_color, relief=RAISED, borderwidth=1 )

        lrow       = 0
        lcol       = 0
        rowspan    = 1
#        a_spacer  = Frame( a_frame, width=60, height=60, bg ="green", relief=RAISED, borderwidth=1 )
#        a_spacer.grid( row = 0, column = lcol, sticky = E + W + N + S, rowspan = 2 )
        # live graph checkbox

        widget_var   = IntVar()
        a_widget     = Checkbutton( a_frame, text="Live Graph", variable = widget_var, width = 10, anchor="w" )
        a_widget.config( command = self.controller.cb_graph_live  )
        a_widget.config( borderwidth = 5, relief = RAISED,  )
        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )
        self.graph_live_var   = widget_var
        lcol +=  1

#        # button to save graph data to csv file not implemented !!
#        a_widget = Button( a_frame , width = 10, height = 1, text = "Save CSV" )
#        a_widget.config( command = self.controller.cb_csv )
#        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )
#        lcol   +=  1
#
#        # button to save graph data to csv file not implemented !!
#        a_widget = Button( a_frame , width = 10, height = 1, text = "Save DB" )
#        a_widget.config( command = self.controller.cb_csv )
#        a_widget.grid( row = lrow, column = lcol, rowspan = 1, sticky = E + W + N + S )
#        lcol   +=  1

        lcol    = 0
        lrow   += 1
        bw_for_db      = FileBrowseWidget( a_frame )
        bw_for_db.grid( row = lrow, column = lcol, columnspan = 1 )
        bw_for_db.set_text( AppGlobal.parameters.db_file_name )
        self.bw_for_db = bw_for_db  # save reference
        lcol   += 1

        return  a_frame

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

        s_text0 = Scrollbar( iframe  )
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
        self.cb_scroll_var  = IntVar()  # for check box in reciev frame
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
        will block until destroyed, except for polling method in controller
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
    def get_db_file_name( self, ):
        """
        what it says
        its name, return a string
        """
        #bw_for_db.set_text     = AppGlobal.parameters.db_file_name
        # x = 1/0   # think should get directly from AppGlobal
        return( self.bw_for_db.get_text() )

    # ------------------------------------------
    def print_send_string( self, data ):
        """
        obsolete fix name !!
        add receive tag to parameters ??
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
    def print_info_string( self, data, update_now = False ):
        """
        add info prefix and new line suffix and show in receive area
        """
        sdata = self.prefix_info +  data  + "\n"    # how did data get to be an int and cause error ??
        self.display_string( sdata, update_now )
        return

    # ------------------------------------------
    def print_no_pefix_string( self, data ):
        """
        add new line suffix and show in receive area
        """
        sdata = data  + "\n"
        self.display_string( sdata )
        return

    # ---------------------------------------
    def display_string( self, a_string, update_now = False ):
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
#            msg     = "Delete from test area at " + str( cut )
#            self.logger.info( msg )

        if self.cb_scroll_var.get():
            self.rec_text.see( END )

        if update_now:
            self.root.update()
        return

#        process devices check box action, see lambda setup in button creation
#        this may be more indirect than needed, go straight to controller ??
        """
#        print( f"cb_device_action {button_ix}, {action}" )--

        self.controller.cb_device_action( button_ix, action  )

#    # ------------------------------------------
#    def display_device_label( self, msg, device_adapter  ):
#        """
#        not needed ?? done by actions directly in device adapter
#        display msg in the device's label area
#        """
#        label       = device_adapter.gui_tk_label
#        label.config( text = msg )

    #----- buttons ------------------------
     # ----------------------------------------
    def cb_device_cb_action( self, button_ix, action  ):
        """

        """
        pass
    # ------------------------------------------
    def cb_device_action( self, button_ix, action  ):
        """
        process devices perhaps on, off timer, see lambda setup in button creation
        this may be more indirect th
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
        #an needed, go straight to controller ??

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
            data  = self.rec_text.get( 1.0, END )
            pyperclip.copy( data )
            return

        elif btext == "Cvert":
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
        clear the message area
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
        pass, not needed, place holder see
        """
        # print "do_auto_scroll"
        # not going to involve controller
        pass
        return

    # ------------------------------------------
    def cb_send_button( self, event ):
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

# -----------------------------------------
class FileBrowseWidget( Frame ):
    """
    let user pick a file name on their computer
    not sure why making it into a widget is a good idea but here goes
    this is a widget that both holds a filename
    and lets you browse to a file
    how is it different from just a couple of widgets
    in your frame ... more reusable ?
    better looking or what
    see graph_smart_plug gui for a use
    !! code is duplicated in 2 guis, this should be fixed
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
        """
        Tk().withdraw()
        filename     = askopenfilename(  initialdir   = "./",
                                         title        = "Select file for db",
                                         filetypes    = (("database files","*.db"),("all files","*.*")))

        if filename == "":
            return

        self.set_text( filename )
        print( f"get_text = {self.get_text()}", flush = True )

        ## AppGlobal.db_file_name   = filename bad idea

    # ------------------------------------------
    def set_text( self, a_string ):
        """
        get the text from the entry
        """
        self.a_string_var.set( a_string )

    # ------------------------------------------
    def get_text( self, ):
        """
        get the text from the entry
        """
        a_string   =  self.a_string_var.get(  )
        return( a_string )

# =======================================

if __name__ == '__main__':
    """
    run the app
    """
    import smart_plug
    a_app = smart_plug.SmartPlug(  )


