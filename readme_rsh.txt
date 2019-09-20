D:\Russ\0000\python00\python3\_projects\smart_plug\readme_rsh.txt


this is mostly a scratch file for notes and output that really belong somewhere else




====================== Notes ==========================

adding DateEntry to the gui, pip install


======================History To Do ================================
** = when done   !! = planned or considerd ?? = think about


?? should i be using from tkinter.scrolledtext import ScrolledText

?? live graph -- research

       self.starting_dir   = os.getcwd()

!! fix time
** create empty db
** export csv
*! coordinate function calls in 2 apps, get into Python convention
!! initial db file name needs to be full path if it is not in the parameter file

!! add device name to graph
** add save graph ( on window )
** units and zero
!! make several devices on seperate graphs
*! needs better error mangaement

for time see parameters.py

right now ( maybe ) unit conversion is supported only for the time axis
units that are available ( parameters.py   )





-------------------- wiki ---------------------

[[Python Control of Smart Plugs]], [[Python Smart Terminal]], [[Python Smart Terminal Graph]], and other programs.

The main page for this project is: [[Python Smart Terminal]].

== Links ==
=== Projects Using these Conventions ===
=== Other Links ===
*Use wiki feature "What Links Here".
*[[Configuration Files For Python]]

<!-----------

this cannot bee seen
------------->

for using the tplink smart plug

functions  - at open circuits


================  Help File =========================
should all be at the open circuits wiki

stuff below will go away

wiki info should eventually be in .\wiki_etc





================ Table of Contents =======================

Application Features
First Use of the SmartPlug Application
How to Use the Parameter File




======================= Working With Database Files ====================

* Create a directory for your data and database -- application comes with defaults


* Run database definition routine   button wf1
       You need to name a database, application will default
       You also need your sample file input, start with the one from
       the step above.
       look at output.......



====================== Debugging ====================


        Watch the console for error messages and in particular look for modules that may be missing ( I do not provide these, pip or conda should install them )



= Work Flow Overview =

================= Just a bit of theory the may be helpful - Some Definitions =

Databases
    These encode data in a structured and efficiently searchable format.  It also easily select subsets of
    data and can sort those results.  There are lots of different kinds, but one fairly standard one is a SQL or
    relational database.

Database File
    The file ( or one of the files ) where database information is kept.  We are using sqllite, which keeps a whole database
    in one file.  This makes it very easy to move and/or backup a database.

Table, Record, Column
    in a SQL data base data is stored in Tables ( many tables may be put in one database ).  A table consists of records ( also called rows. )  Each row is information about some "thing".  For example if the "thing" is a person a record
    might contain the person's first name, last name, date of birth.... The table is much like a spread sheet with
    the information on each person in a row.  Each of the items ( first name, last name, date of birth.... ) is called a column.

SQL - Structured Query Language
    This is the language used by relational databases.  Typically the system generated the required SQL and runs
    it.  The user interface often shows the SQL which is quite a bit easier to read than it is to write.
    It may give you useful feedback on what the system is doing.


readme_rsh.txt for the smartplug_graph
D:\Russ\0000\python00\python3\_projects\smart_plug_graph\Ver2\readme_rsh.txt

Author: Russ Hensel
github: ??

======================= Status ========================


Runs but largely not working .... gui appears but lots of bogus stuff



======================= to do =======================


** create empty db
** export csv

!! initial db file name needs to be full path if it is not in the parameter file

!! add device name to graph
** add save graph ( on window )
** units and zero
!! make several devices on seperate graphs


for time see parameters.py

right now ( maybe ) unit conversion is supported only for the time axis
units that are available ( parameters.py   )




====================== Notes ==========================

adding DateEntry to the gui, pip instlled


======================History To Do ================================
** = when done   !! = planned or considerd ?? = think about

!! live graph -- research

       self.starting_dir   = os.getcwd()
	   
	   
	   readme_rsh.txt for the smartplug_graph
D:\Russ\0000\python00\python3\_projects\smart_plug_graph\Ver2\readme_rsh.txt

Author: Russ Hensel
github: ??

======================= Status ========================


Runs but largely not working .... gui appears but lots of bogus stuff



======================= to do =======================


** create empty db
** export csv

!! initial db file name needs to be full path if it is not in the parameter file

!! add device name to graph
** add save graph ( on window )
** units and zero
!! make several devices on seperate graphs


for time see parameters.py

right now ( maybe ) unit conversion is supported only for the time axis
units that are available ( parameters.py   )




====================== Notes ==========================

adding DateEntry to the gui, pip instlled


======================History To Do ================================
** = when done   !! = planned or considerd ?? = think about

!! live graph -- research

       self.starting_dir   = os.getcwd()

========================= Dead Code ========================================================


------------------- db and mode settings -------------




========================= Dead Code ========================================================


------------------- db and mode settings -------------









========================= Dead Code ========================================================





'info'     : '{"system":{"get_sysinfo":{}}}',
			'on'       : '{"system":{"set_relay_state":{"state":1}}}',
			'off'      : '{"system":{"set_relay_state":{"state":0}}}',
			'cloudinfo': '{"cnCloud":{"get_info":{}}}',
			'wlanscan' : '{"netif":{"get_scaninfo":{"refresh":0}}}',
			'time'     : '{"time":{"get_time":{}}}',
			'schedule' : '{"schedule":{"get_rules":{}}}',
			'countdown': '{"count_down":{"get_rules":{}}}',
			'antitheft': '{"anti_theft":{"get_rules":{}}}',
			'reboot'   : '{"system":{"reboot":{"delay":1}}}',
			'reset'    : '{"system":{"reset":{"delay":1}}}',
			'energy'   : '{"emeter":{"get_realtime":{}}}'


#Commands:
#  alias          Get or set the device alias.
#  brightness     Get or set brightness.
#  discover       Discover devices in the network.
#  dump-discover
#  emeter         Query emeter for historical consumption.
#  hsv            Get or set color in HSV.
#  led            Get or set (Plug's) led state.
#  off            Turn the device off.
#  on             Turn the device on.
#  raw-command    Run a raw command on the device.
#  reboot         Reboot the device.
#  state          Print out device state and versions.
#  sysinfo        Print out full system information.
#  temperature    Get or set color temperature.
#  time           Get the device time.
#



has_emeter


sysinfo
location


macaddress

get_emeter_realtime(self) -> EmeterStatus:
        """Retrive current energy readings.

        :returns: current readings or False

    def get_emeter_daily(
        self, year: int = None, month: int = None, kwh: bool = True
    ) -> Dict:
        """Retrieve daily statistics for a given month.

        :param year: year for which to retrieve statistics (default: this year)
        :param month: month for which to retrieve statistics (default: this
                      month)
        :param kwh: return usage in kWh (default: True)
        :return: mapping of day of month to value
                 None if device has no energy meter or error occurred
        :rtype: dict
        :raises SmartDeviceException: on error


    def erase_emeter_stats(self) -> bool:
        """Erase energy meter statistics.

        :return: True if statistics were deleted
                 False if device has no energy meter.
        :rtype: bool
        :raises SmartDeviceException: on error






--------------------------- bit of trace for sys_info ..............................

self.sys_info  defined in smartdeice   def get_sysinfo(self) -> Dict:    _query_helper()

        return self._query_helper("system", "get_sysinfo")


     if self.context is None:
                request = {target: {cmd: arg}}
            else:
                request = {"context": {"child_ids": [self.context]}, target: {cmd: arg}}


            response = self.protocol.query(host=self.host, request=request)




TP-LINK HS110 Smart Plug w/Energy Monitoring



TP-LINK HS110 Smart Plug w/Energy Monitoring - - Amazon.com
    *>url  https://www.amazon.com/gp/product/B0178IC5ZY/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1

(29) What I have been up to lately - YouTube
    *>url  https://www.youtube.com/watch?v=uBaz9RBbHOo

TP-LINK HS110 python - Google Search
    *>url  https://www.google.com/search?q=TP-LINK%20HS110%20python

GitHub - GadgetReactor/pyHS100: Python Library to control TPLink Switch (HS100 / HS110)
    *>url  https://github.com/GadgetReactor/pyHS100

Topic: hs110 · GitHub
    *>url  https://github.com/topics/hs110

GitHub - softScheck/tplink-smartplug: TP-Link WiFi SmartPlug Client and Wireshark Dissector
    *>url  https://github.com/softScheck/tplink-smartplug

GitHub - ajay10000/TP-Link-HS110: TP-Link Wi-Fi Smart Plug Protocol Client
    *>url  https://github.com/ajay10000/TP-Link-HS110

Reverse Engineering the TP-Link HS110 | softScheck
    *>url  https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/

python-tplink-smarthome · PyPI
    *>url  https://pypi.org/project/python-tplink-smarthome/

pyHS100 · PyPI
    *>url  https://pypi.org/project/pyHS100/

Collect and store realtime data from the TP-LINK HS110
    *>url  https://www.beardmonkey.eu/tplink/hs110/2017/11/21/collect-and-store-realtime-data-from-the-tp-link-hs110.html

TPlink-PoSH/TPlinkPlugControlNew.ps1 at master · EgoManiac/TPlink-PoSH
    *>url  https://github.com/EgoManiac/TPlink-PoSH/blob/master/TPlinkPlugControlNew.ps1

Collect and store realtime data from the TP-LINK HS110
    *>url  https://www.beardmonkey.eu/tplink/hs110/2017/11/21/collect-and-store-realtime-data-from-the-tp-link-hs110.html

(29) What I have been up to lately - YouTube
    *>url  https://www.youtube.com/watch?v=uBaz9RBbHOo

TP-LINK HS110 python - Google Search
    *>url  https://www.google.com/search?q=TP-LINK%20HS110%20python

GitHub - GadgetReactor/pyHS100: Python Library to control TPLink Switch (HS100 / HS110)
    *>url  https://github.com/GadgetReactor/pyHS100#pyhs100

GitHub - softScheck/tplink-smartplug: TP-Link WiFi SmartPlug Client and Wireshark Dissector
    *>url  https://github.com/softScheck/tplink-smartplug

Reverse Engineering the TP-Link HS110 | softScheck
    *>url  https://www.softscheck.com/en/reverse-engineering-tp-link-hs110/

GitHub - ajay10000/TP-Link-HS110: TP-Link Wi-Fi Smart Plug Protocol Client
    *>url  https://github.com/ajay10000/TP-Link-HS110

python-tplink-smarthome · PyPI
    *>url  https://pypi.org/project/python-tplink-smarthome/

pyHS100 · PyPI
    *>url  https://pypi.org/project/pyHS100/

Collect and store realtime data from the TP-LINK HS110
    *>url  https://www.beardmonkey.eu/tplink/hs110/2017/11/21/collect-and-store-realtime-data-from-the-tp-link-hs110.html

pyHS100 discover not working - Google Search
    *>url  https://www.google.com/search?q=pyHS100+discover+not+working&oq=pyHS100+discover+not+working&aqs=chrome..69i57.7503j0j0&sourceid=chrome&ie=UTF-8

HS105 support · Issue #18 · GadgetReactor/pyHS100 · GitHub
    *>url  https://github.com/GadgetReactor/pyHS100/issues/18

Tp-Link manually add ip - Mozilla IoT - Mozilla Discourse
    *>url  https://discourse.mozilla.org/t/tp-link-manually-add-ip/32152

-------------------------------------------------------------------------------------------------
info, not much use #


 !!! {'sw_ver': '1.2.5 Build 171206 Rel.085954',
 'hw_ver': '1.0', 'mac': 'D8:0D:17:C5:98:90',
 'type': 'IOT.SMARTPLUGSWITCH',
 'hwId': '60FF6B258734EA6880E186F8C96DDC61',
 'fwId': '00000000000000000000000000000000',
 'oemId': 'FFF22CFF774A0B89F7624BFC6F50D5DE',
 'dev_name': 'Wi-Fi Smart Plug With Energy Monitoring'}



192.168.0.209

On	192.168.0.209	192.168.0.209									TP-LINK TECHNOLOGIES CO.	LTD.	D8:0D:17:C5:98:90
== joe - HS110(US) ==
OFF
Host/IP: 192.168.0.209
LED state: True
On since: 2019-08-20 12:50:25.549754
== Generic information ==
Time:         2019-08-20 12:50:24
Hardware:     1.0
Software:     1.2.5 Build 171206 Rel.085954
MAC (rssi):   D8:0D:17:C5:98:90 (-51)
Location:     {'latitude': 41.540025, 'longitude': -71.010105}
== Emeter ==
== Current State ==
{'current': 0.013811, 'voltage': 124.997428, 'power': 0, 'total': 0}

(base) D:\Russ\0000\python00\python3\_projects\smart_plug>






------------------------------ from easy db -------------------------


ex_sql_lite


    # ----------------- Buttons start with bcb buttons -----------------
    # ----- define table  ready for rename !!
    def bcb_define_table( self ):  # place holder for function not yet determined

#        msg   = "\n"*2 +"tbd_bcb_wf_1 define_table"
#        print( msg )
#        self.write_gui( msg  )
#        self.try_make_and_run_table_def_sql( self.add_data_path( self.parameters.db_file_name ),
#                                             self.add_data_path( self.parameters.filein_name ), )

        db_file_name  = AppGlobal.db_file_name
        in_file_name  = AppGlobal.filein_name

        msg  = "Define Table"
        AppGlobal.gui_write_start( msg )
        try:
            table_info   = db_objects.TableInfo( )
            table_info.build_from_input_file( in_file_name,  print_out=True )
            #print( table_info.to_sql() )
            table_access  = db_objects.TableAccess( db_file_name, table_info  )
            table_access.define_table_from_table_info()
            # success  # refresh db file
            self.change_table_name( table_info.table_name )
#            temp                    = AppGlobal.db_file_name
#            AppGlobal.db_file_name  = None
#            self.change_db_file_name( temp )

            msg    = f"... new table defined: {table_info.table_name}"
            self.write_gui( msg )
        except db_objects.DBOjectException as exception:
            print( exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg  = "Define Table"
        AppGlobal.gui_write_finish( msg )

    # -------------------------------




    -------------------
# ====================== gui events ============
    # ----------------------------------
    def change_db_file_name( self, new_db_file_name ):
        """
        a gui event, change if valid and different
        also changes data_dir
        can use at init as well
        """
        # old file name
        if AppGlobal.db_file_name == new_db_file_name:
            return
        # !! still need to validate
        # need to extract data dir  -- or move to input file functions below
        data_dir          = os.path.dirname(  new_db_file_name )

        msg               = f"change_db_file_name {new_db_file_name} {data_dir}"
        AppGlobal.print_debug( msg )

        tables            = db_objects.get_table_list( new_db_file_name )
        if tables is None:
            tables = []
            msg               = f"tables is None {new_db_file_name} "
            AppGlobal.print_debug( msg )

        if tables ==  []:
            return
        self.gui.ddw_tables.set_list( tables )
        self.gui.ddw_tables.set_index( 0 )
        #self.gui.ddw_tables.set_text( "test set_text" )

        self.gui.set_db_file_name( new_db_file_name )
        AppGlobal.db_file_name   = new_db_file_name
        AppGlobal.data_dir       = data_dir
        table_name               = self.gui.ddw_tables.get_text()
        self.change_table_name( table_name )

    # ----------------------------------
    def change_last_output_file_name( self, new_file_name ):
        """
        a gui event, change if valid and different
        also changes data_dir
        can use at init as well
        """
        # old file name
#        if AppGlobal.last_output_file_name == new_file_name:
#            return
        # !! still need to validate
        # need to extract data dir  -- or move to input file functions below
        AppGlobal.last_output_file_name = new_file_name

        msg               = f"change_last_output_file_name {new_file_name}"
        AppGlobal.print_debug( msg )

        self.gui.last_output_file_name_label.config( text = f"Last Output:{new_file_name}" )

   # ----------------------------------
    def change_input_file_name( self, new_file_name ):
        """
        a gui event, change if valid and different
        also changes data_dir
        can use at init as well
        """
        # old file name
        if AppGlobal.filein_name == new_file_name:
            return
        # !! still need to validate
        # need to extract data dir
#        data_dir          = os.path.dirname(  new_db_file_name )
#        tables            = db_objects.get_table_list( new_db_file_name )
#        if tables is None:
#            tables = []
#
#        self.gui.ddw_tables.set_list( tables )

#        self.gui.set_db_file_name( new_db_file_name )
        AppGlobal.filein_name   = new_file_name
#        AppGlobal.data_dir       = data_dir

   # ----------------------------------
    def change_table_name( self, table_name ):
        """
        a gui event, change if valid and different
        can use at init as well
        self.controller.change_table_name( table_name )
        """
        msg     = f"change_table_name =>>{table_name}<<"
        AppGlobal.print_debug( msg )
#        if AppGlobal.table_name  == table_name:  # may not be necessary
#            return
        AppGlobal.table_name      = table_name
        AppGlobal.gui.ddw_tables.set_text( table_name )

   # ----------------------------------
    def change_select_file_name( self, new_file_name ):
        """
        a gui event, change if valid and different
        can use at init as well
        """
        msg     = f"change_select_file_name =>>{new_file_name}<<"
        AppGlobal.print_debug( msg )
#        if AppGlobal.select_file_name     == new_file_name:
#            return
        AppGlobal.select_file_name         = new_file_name
        AppGlobal.gui.set_select_file_name(  new_file_name )

    # ----------------------------------
    def setup_table_info( self, ):
        """
        store some data dict info, this may be a short term thing
        """
        self.parameters.make_table_info_room( )
        self.parameters.make_table_info_observation( )
        self.parameters.make_table_info_mush( )

    # ----------------- Buttons start with bcb buttons -----------------
    # ----- define table  ready for rename !!
    def bcb_define_table( self ):  # place holder for function not yet determined

#        msg   = "\n"*2 +"tbd_bcb_wf_1 define_table"
#        print( msg )
#        self.write_gui( msg  )
#        self.try_make_and_run_table_def_sql( self.add_data_path( self.parameters.db_file_name ),
#                                             self.add_data_path( self.parameters.filein_name ), )

        db_file_name  = AppGlobal.db_file_name
        in_file_name  = AppGlobal.filein_name

        msg  = "Define Table"
        AppGlobal.gui_write_start( msg )
        try:
            table_info   = db_objects.TableInfo( )
            table_info.build_from_input_file( in_file_name,  print_out=True )
            #print( table_info.to_sql() )
            table_access  = db_objects.TableAccess( db_file_name, table_info  )
            table_access.define_table_from_table_info()
            # success  # refresh db file
            self.change_table_name( table_info.table_name )
#            temp                    = AppGlobal.db_file_name
#            AppGlobal.db_file_name  = None
#            self.change_db_file_name( temp )

            msg    = f"... new table defined: {table_info.table_name}"
            self.write_gui( msg )
        except db_objects.DBOjectException as exception:
            print( exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg  = "Define Table"
        AppGlobal.gui_write_finish( msg )

    # -------------------------------
    def bcb_select_using_file( self, ):
        """

        """
        db_file_name         = AppGlobal.db_file_name
        input_file_name      = AppGlobal.select_file_name

        output_format        = AppGlobal.gui.ddw_format.get_text( ),

        try:

            msg     = f"Begin select using file: {input_file_name} for format {output_format}"
            AppGlobal.gui_write_start( msg )
#            msg     = ( "\n"*2 + f"========= bcb_select_using_file(  ) =================" )
#            AppGlobal.print_debug( msg )
#            msg     = f"bcb_select_using_file args {db_file_name} {input_file_name} {output_format} db >>{db_file_name}<<"
#            AppGlobal.print_debug( msg )

            table_info    = db_objects.TableInfo( )

            table_info.build_select_sql_from_file( db_file_name, input_file_name, print_out=False )  # needed for file writer

            AppGlobal.print_debug( table_info )

            output_format   = AppGlobal.gui.ddw_format.get_text()
            if  output_format == "py_log":
                fileout_name      = self.add_data_path( "select_output.txt"  )
                select_writer     = file_writers.SelectLogWriter(    None,         table_info )

            elif output_format == "input":
                fileout_name      = self.add_data_path( "select_output.txt"  )
                select_writer     = file_writers.SelectExportWriter( fileout_name, table_info )

            elif output_format == "csv":
                fileout_name      = self.add_data_path( "select_output.csv"  )
                select_writer     = file_writers.SelectCSVWriter( fileout_name, table_info )

            elif output_format == "table":
                fileout_name      = self.add_data_path( "select_output_table.txt"  )
                select_writer     = file_writers.SelectTableWriter( fileout_name, table_info )

            else:
                msg   =  f"invalid output_format = {output_format}"
                AppGlobal.write_gui( msg )
                AppGlobal.print_debug( msg )
                raise db_objects.DBOjectException( msg )

            table_access      = db_objects.TableAccess( db_file_name, table_info )
            table_access.run_info_sql_with_writer( select_writer )

            self.change_table_name( table_info.table_name )

            if  output_format == "py_log":
                self.os_open_text_file( self.parameters.pylogging_fn   )
                self.change_last_output_file_name( self.parameters.pylogging_fn )
            else:
                self.os_open_text_file( fileout_name  )   # or log
                self.change_last_output_file_name( fileout_name )

        except db_objects.DBOjectException as exception:

            AppGlobal.print_debug( exception.msg )
            AppGlobal.write_gui(   exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg     = "Select complete"
        AppGlobal.gui_write_finish( msg )

    # ----------------------------------
    def bcb_insert_file( self ):  # place holder for function not yet determined

        text_file_name     = AppGlobal.filein_name
        db_file_name       = AppGlobal.db_file_name
        #fileout_name       = self.add_data_path( self.parameters.fileout_name )
        msg     = f"Insert from file {text_file_name}"
        AppGlobal.gui_write_start( msg )
        try:
            file_reader        = file_readers.FileReader( text_file_name, db_file_name,     )
            file_reader.insert_from_file(  )
            self.change_table_name( file_reader.table_info.table_name )

        except db_objects.DBOjectException as exception:

            AppGlobal.print_debug(       exception.msg )
            AppGlobal.gui_write_error(   exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn )

        msg     = "Insert from file complete"
        AppGlobal.gui_write_finish( msg )

    # ----------------------------------
    def bcb_make_table_form(self ):
        """
        button call back, see name
        """
        try:
            db_file_name      = AppGlobal.db_file_name
            table_name        = AppGlobal.table_name
            msg  = f"Make Table Form ( data input form ) for {table_name}"
            AppGlobal.gui_write_start( msg )
            output_file_name  = self.add_data_path( f"input_form_for_{table_name}.txt" )
            #self.test_make_table_form( db_file_name,  table_name, output_file_name )

            table_access  = db_objects.TableAccess( db_file_name,  None )
            table_access.init_table_info_from_db( table_name )
            table_access.make_table_form( output_file_name )
            self.change_last_output_file_name( output_file_name )
            self.os_open_text_file( output_file_name  )

        except db_objects.DBOjectException as exception:
            AppGlobal.print_debug( exception.msg )
            self.gui_write_error(  exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg  = "Make Table Form done"
        AppGlobal.gui_write_finish( msg )

    #-----------------------------------
    def bcb_make_select_form (self ):
        """
        button call back, see name
        """
        table_name       = AppGlobal.table_name
        db_file_name     = AppGlobal.db_file_name

        msg  = f"Make Select Form for table {table_name}"
        AppGlobal.gui_write_start( msg )

        output_file_name = f"{table_name}_select_form.txt"
        output_file_name = self.add_data_path( output_file_name )
        try:
            table_info       = db_objects.TableInfo( )
            table_info.build_from_db_file( table_name, db_file_name, print_out=False )

            file_writer     = file_writers.SelectFormWriter( output_file_name, table_info )
            file_writer.write_file()
            self.change_last_output_file_name( output_file_name )
            self.os_open_text_file( output_file_name   )

        except db_objects.DBOjectException as exception:
            AppGlobal.print_debug( exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg  = "Done Make Select Form"
        AppGlobal.gui_write_finish( msg )

    # ----------------------------------
    def bcb_delete_all(self ):

        db_file_name    = AppGlobal.db_file_name
        table_name      = AppGlobal.current_table

        msg  = "Delete all rows for table {table_name}"
        AppGlobal.gui_write_start( msg )
        AppGlobal.print_debug( msg )

        try:
            table_access  = db_objects.TableAccess( db_file_name,  None )
            table_access.init_table_info_from_db( table_name )   # convienienbce
            table_access.delete_all(  )

        except db_objects.DBOjectException as exception:
            AppGlobal.print_debug( exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg  = "Done Delete all rows"
        AppGlobal.gui_write_finish( msg )

    # --------- end bcb  -------------------------
    # ----------------------------------
    def tbd_bcb_wf_2( self ):  # place holder for function not yet determined
        pass
        print( "tbd_bcb_wf_2" + " check_file" )

        self.try_check_file(  AppGlobal.filein_name,
                              AppGlobal.db_file_name, )

    #--------------------------------
    def try_check_file( self, file_name_to_check, db_file_name ):
        """
        checks against the data_info, table must have been defined first
        uses
        """
        msg    = f"========= try_check_file( file_name = {file_name_to_check} ) ================="
        print(  "\n"*2 + msg )
        self.write_gui( msg  )

        file_reader     = file_readers.FileReader( file_name_to_check, db_file_name,   )      #FileReader
        #file_reader.data_object.set_data_info( AppGlobal.data_info )

        errors   =  file_reader.check_file( 10 )   # 10 is max errors
        msg      = f"check insert file, errors = {errors}"
        self.write_gui( msg  )



    # ----------------------------------
    def tbd_bcb_wf_4a(self ):  # place holder for function not yet determined
        pass
        print( "tbd_bcb_wf_4" + "select all" )
#        self.setup_table_info()
#        AppGlobal.print_info()
        self.try_select_all( self.add_data_path( self.parameters.db_file_name ),
                                  self.parameters.default_table_name,
                                  self.add_data_path( "select_output.csv"  )
                                  )

    #--------------------------------
    def try_select_all( self,  db_file_name, table_name, fileout_name ):
        """
        db and table must be defined first
        SelectLogWriter
        """
        print("\n"*2)
        print( f"========= try_select_all_rows( {db_file_name} {table_name} {fileout_name} ) =================")

        # choose a writer
        select_writer     = file_writers.SelectLogWriter(    None,         None )
        select_writer     = file_writers.SelectExportWriter( fileout_name, None )

        table_access      = db_objects.TableAccess( db_file_name,  None )
        table_access.init_table_info_from_db( table_name )

        # -----0 with select all
        sql_where        = ""
        values_where     = tuple( [] )
        table_access.select_all_cols( sql_where, values_where,  order_by = "", select_writer = select_writer )

        self.os_open_text_file( fileout_name  )   # or log

    # ----------------------------------
    def tbd_bcb_wf_4(self ):  # place holder for function not yet determined
        pass
        print( "tbd_bcb_wf_4" + "select" )
#        self.setup_table_info()
#        AppGlobal.print_info()
        self.try_select( self.add_data_path( self.parameters.db_file_name ),
                                  self.parameters.default_table_name,
                                  self.add_data_path( self.parameters.fileout_name  )
                                  )

    #--------------------------------
    def try_select( self,  db_file_name, table_name, fileout_name ):
        """
        select controlled by various items coded here, not by a file
        db and table must be defined first
        SelectLogWriter
        """
        print( "\n"*2 + f"========= try_select_all_rows( {db_file_name} {table_name} {fileout_name} ) =================")
        #AppGlobal.print_info()

        select_writer     = file_writers.SelectLogWriter(    None,         None )
        select_writer     = file_writers.SelectExportWriter( fileout_name, None )

        table_access      = db_objects.TableAccess( db_file_name,  None )
        table_access.init_table_info_from_db( table_name )

#        -----0 with select all
#        table_access.select_all_cols( sql_where, values_where,  order_by = "", select_writer = select_writer )

       #----- select all a different way with order by
        sql_where        = ""
        values_where     = tuple( [] )
        #        ORDER BY column1, column2, ... ASC|DESC;    , "ORDER BY bot_name ASC",  ....more...
        order_by         = "ORDER BY bot_name ASC"
        order_by         = ""
        table_access.select_all_cols( sql_where, values_where,  order_by = order_by, select_writer = select_writer )


        self.os_open_text_file( fileout_name  )   # or log

    # ----------------------------------
    def bcb_delete_select(self ):  # place holder for function not yet determined
        pass
        print( "bcb_delete_select" )

        db_file_name         = AppGlobal.db_file_name
        input_file_name      = AppGlobal.select_file_name

#        output_format        = AppGlobal.gui.ddw_format.get_text( ),

        try:

            msg     = f"Begin delete using file: {input_file_name}"
            AppGlobal.gui_write_start( msg )
#            msg     = ( "\n"*2 + f"========= bcb_select_using_file(  ) =================" )
#            AppGlobal.print_debug( msg )
#            msg     = f"bcb_select_using_file args {db_file_name} {input_file_name} {output_format} db >>{db_file_name}<<"
#            AppGlobal.print_debug( msg )

            table_info    = db_objects.TableInfo( )

            #table_info.build_select_sql_from_file( db_file_name, input_file_name, print_out=False )  # needed for file writer
            table_info.build_delete_sql_from_file( db_file_name, input_file_name )
            AppGlobal.print_debug( table_info )

#            output_format   = AppGlobal.gui.ddw_format.get_text()
#            if  output_format == "py_log":
#                fileout_name      = self.add_data_path( "select_output.txt"  )
#                select_writer     = file_writers.SelectLogWriter(    None,         table_info )
#
#            elif output_format == "input":
#                fileout_name      = self.add_data_path( "select_output.txt"  )
#                select_writer     = file_writers.SelectExportWriter( fileout_name, table_info )
#
#            elif output_format == "csv":
#                fileout_name      = self.add_data_path( "select_output.csv"  )
#                select_writer     = file_writers.SelectCSVWriter( fileout_name, table_info )
#
#            elif output_format == "table":
#                fileout_name      = self.add_data_path( "select_output_table.txt"  )
#                select_writer     = file_writers.SelectTableWriter( fileout_name, table_info )
#
#            else:
#                msg   =  f"invalid output_format = {output_format}"
#                AppGlobal.write_gui( msg )
#                AppGlobal.print_debug( msg )
#                raise db_objects.DBOjectException( msg )


            table_access      = db_objects.TableAccess( db_file_name, table_info )
            table_access.run_info_sql(  )


            self.change_table_name( table_info.table_name )

#            if  output_format == "py_log":
#                self.os_open_text_file( self.parameters.pylogging_fn   )
#                self.change_last_output_file_name( self.parameters.pylogging_fn )
#            else:
#                self.os_open_text_file( fileout_name  )   # or log
#                self.change_last_output_file_name( fileout_name )

        except db_objects.DBOjectException as exception:

            AppGlobal.print_debug( exception.msg )
            AppGlobal.write_gui(   exception.msg )
            self.os_open_text_file( self.parameters.pylogging_fn   )

        msg     = "Delete complete"
        AppGlobal.gui_write_finish( msg )

#    #--------------------------------
#    def try_delete_all( self,  db_file_name, table_name ):
#        """
#        db and table must be defined first
#        """
#        msg     = "\n"*2 + f"========= tbd_bcb_wf_5: try_delete_all( {db_file_name} { table_name} ) ================="
#        AppGlobal.print_debug( msg )
#        AppGlobal.write_gui( msg  )
#        #AppGlobal.print_info()
#        table_access  = db_objects.TableAccess( db_file_name,  None )
#        table_access.init_table_info_from_db( table_name )   # convienienbce
#        table_access.delete_all(  )
#        msg     =  f"========= delete_all complete( {db_file_name}  ================="
#        AppGlobal.print_debug( msg )
#        AppGlobal.write_gui( msg  )
##        if out_file_name is not None:
##             self.os_open_text_file( out_file_name )

    # ----------------------------------
    def tbd_bcb_wf_6(self ):
        """
        select controlled by a file
        """
        pass
        print( "tbd_bcb_wf_6 select controlled by a file" )

    # ----------------------------------
    def tbd_bcb_wf_7(self ):
        """
        edit part a
        """
        msg     = "tbd_bcb_wf_7 edit part a"
        print( msg )
        self.write_gui( msg  )
        self.test_edit_one_record_a(  self.add_data_path( self.parameters.db_file_name ),
                        "mush", "Cantharellus lateritius",
                        self.add_data_path( self.parameters.edit_file_name ) )

    # ----------------------------------
    def test_edit_one_record_a( self, db_file_name, table_name, record_key, edit_file_name ):
        """

        """
        msg   = "\n"*2 +f"========= test_edit_one_record_a( {db_file_name}, {table_name}, {record_key} )  "
        print( msg )
        self.write_gui( msg  )

        print( f"  ==========  try_edit_one_record_b( {edit_file_name},   ) =================")

        table_access  = db_objects.TableAccess( db_file_name,  None )
        table_access.init_table_info_from_db( table_name )

        table_access.edit_one_record_1( record_key, edit_file_name )








 #--------------------------------
if __name__ == "__main__":

    app = App( )

# ======================= eof =======================





