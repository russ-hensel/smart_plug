# -*- coding: utf-8 -*-


"""
Purpose:
    define a smart plug db, this is a utility
    now part of the application
    working with partly implemented stuff
    and old crud still hanging around



"""

import sqlite3 as lite
#import sys

# ----------- local imports --------------------------

# import parameters
from   app_global import AppGlobal


# ----------------------------------------------
def create_db( db_file_name, overwrite = False ):
    """
    try to create tables, no exceptions but return error message not "" if error
    overwrite not implemented
    """
    error_msg    = create_table_plug_measurements( db_file_name )
    if not(  error_msg == "" ):
        return error_msg
    error_msg    = create_table_plug_events( db_file_name  )
    return error_msg

# ----------------------------------------------
def create_table_plug_measurements( db_file_name, allow_drop = False ):
    """
    old code from standalone, needs error correct and extension
    allow_drop not implemented
    """
#    print( """============= create_table_plug_measurements() =====================
#
#    """ )
    try:
        sql_con = lite.connect( db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            #cur.execute("DROP TABLE IF EXISTS plug_measurements")   # else error if table exists
            cur.execute("CREATE TABLE plug_measurements( "+
                              " plug_name TEXT, plug_time Real, measure_type TEXT, " +
                              " plug_state TEXT,  voltage REAL,  current REAL, inst_power REAL, total_energy REAL," +
                              " PRIMARY KEY (plug_name, plug_time, measure_type ) )")

    except lite.Error as a_except:
     #except ( lite.Error, TypeError) as a_except:
         print( type(a_except), '::', a_except )
         return "error creating table plug_measurements, exception {a_except}"

    return ""
#create_table_plug_measurements()

# ----------------------------------------------
def create_table_plug_events( db_file_name, allow_drop = False ):
    """
    old code from standalone, needs error correct and extension
    return string, empty if ok, else error message
    """
#    print( """============= create_table() =====================
#
#    """ )
    try:
        sql_con = lite.connect( db_file_name )

        with sql_con:
            cur = sql_con.cursor()
            if allow_drop:
                cur.execute("DROP TABLE IF EXISTS plug_events")   # else error if table exists
            cur.execute("CREATE TABLE plug_events( "+
                              " plug_name TEXT, plug_time Real, event_type TEXT, " +
                              " plug_state TEXT,  voltage REAL,  current REAL, inst_power REAL, total_energy REAL," +
                              " PRIMARY KEY ( plug_name, plug_time, event_type ) )")
    except lite.Error as a_except:
     #except ( lite.Error, TypeError) as a_except:
         print( type(a_except), '::', a_except )
         return "error creating table plug_events, exception {a_except}"

    return ""

#create_table_plug_events()

# ----------------------------------------------
def insert_test_rows():
    print( """============= insert_test_rows() =====================
          table plug_measurements
    """ )
    sql_con = lite.connect( db_file_name )

    with sql_con:
        cur = sql_con.cursor()
        cur.execute( "INSERT INTO plug_measurements VALUES( 'joe', 55796.3, 'm', 'on',  125,   2.3,   250,  37005)")
        cur.execute( "INSERT INTO plug_measurements VALUES( 'joe', 55797.3, 'm', 'off', 125,   2.3,   250,  37008)")

#insert_test_rows()

# ----------------------------------------------
def ex_insert_many_test_rows( db_file_name ):
    print( """============= ex_insert_many_test_rows() =====================
          table plug_measurements
    """ )
    data    =  (('device_1', 1566954050.2703698, 'r', '?', 122.939502, 0.012947, 0, 0.038)  ,  ('device_1', 1566954060.2703698, 'r', '?', 122.939502, 0.012947, 0, 0.038))
    sql_con = lite.connect( db_file_name )

    with sql_con:
        cur = sql_con.cursor()

        sql  = ( "INSERT INTO plug_measurements " +
                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy ) VALUES  " +
                       " ( ?,         ?,         ?,             ?,          ?,       ?,       ?,          ?  )" )

        sql  = ( "INSERT INTO plug_measurements " +
                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy ) VALUES  " +
                       " ( ?,         ?,         ?,             ?,          ?,       ?,       ?,          ?  )" )
        print( f"{sql}" )
        cur.executemany( sql, data )

#        cur.executemany( "INSERT INTO plug_measurements " +
#                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy ) VALUES  " +
#                       " ( ?,         ?,         ?             ?,          ?,       ?,       ?,          ?  )", data  )   # could count the cols
       # cur.executemany( "INSERT INTO Cars ( Id, Name, Price ) VALUES (?, ?, ?)", cars)
      #sql_con.commit()


#insert_many_test_rows()

#(('device_1', 1566954050.2703698, 'r', '?', 122.939502, 0.012947, 0, 0.038),)


# ----------------------------------------------
def ex_create_db( db_file_name ):
    print( """\n============= create_db() =====================
    """ )
    create_db( db_file_name )

# ----------------------------------------------
def ex_select_all_plug_measurements( db_file_name ):
    print( """\n============= ex_select_all_plug_measurements() =====================
    """ )
    #ex_create_table_insert()
    sql_con = lite.connect( db_file_name )
    with sql_con:

        cur = sql_con.cursor()
        cur.execute("SELECT * FROM plug_measurements")

        rows = cur.fetchall()
        for row in rows:
            print( row  )

# ----------------------------------------------
def ex_select_where( db_file_name ):
    print( """============= ex_select_where() =====================
    """ )
    # also not named place holders

    sql_con = lite.connect(  db_file_name  )

    with sql_con:
        plug_name = "device_1"
        cur = sql_con.cursor()

        cur.execute("SELECT ROWID, plug_name, plug_time, measure_type,  plug_state, current, inst_power, total_energy FROM plug_measurements WHERE plug_name=:plug_name",
            {"plug_name": plug_name })
        sql_con.commit()

        # ------ one of following

#        row = cur.fetchone()
#        print ( row[0], row[1], row[2], row[3] )

        rows = cur.fetchall()
        for row in rows:
           # print( row  )
            row_as_list = list( row )
            print( row_as_list )
            del row_as_list[ 0 ]
            #print( row_as_list )
            a_dict   = {}

# ----------------------------------------------
def ex_multiply_data( db_file_name ):
    print( """============= ex_multiply_data() =====================
	make data for a second device using the data from a device already present in the db
	not implemented
    """ )
    # also not named place holders

    sql_con = lite.connect(  db_file_name  )

    with sql_con:
        plug_name = "device_1"
        cur         = sql_con.cursor()
        cur_2       = sql_con.cursor()

        cur.execute("SELECT ROWID, plug_name, plug_time, measure_type,  plug_state, voltage, current, inst_power, total_energy FROM plug_measurements WHERE plug_name=:plug_name",
            {"plug_name": plug_name })
        sql_con.commit()

        # ------ one of following

#        row = cur.fetchone()
#        print ( row[0], row[1], row[2], row[3] )

        rows = cur.fetchall()
        for row in rows:
#            print( row  )
            row_as_list = list( row )
            del row_as_list[ 0 ]   # drop ROWID
            #print( row_as_list )
#            print( row_as_list[5] )
            row_as_list[0] = "device_2"
            row_as_list[5] = max( row_as_list[5] * .6 - 1., 0. )
#            print( row_as_list )
            data = ( tuple( row_as_list ), )
            print( data )

#           data    =  ('device_1', 1566954050.2703698, 'r', '?', 122.939502, 0.012947, 0, 0.038)
            sql  = ( "INSERT INTO plug_measurements " +
                       " ( plug_name, plug_time, measure_type, plug_state, voltage, current, inst_power, total_energy ) VALUES  " +
                       " ( ?,         ?,         ?,             ?,          ?,       ?,       ?,          ?  )" )

            cur_2.executemany( sql, data )

# execute at end not here    ex_multiply_data()


# !! may want to keep options of running from the console -- as well a gui


# ==============================================
if __name__ == '__main__':

    module_db_file_name = "define_db.db"
    module_db_file_name = "test_data.db"  # do no redefine test_data.db
   # module_db_file_name = "test_data_dup.db"
    """
    to run from module
    """
    print( "" )
    print( " ========== define_db as module pick functions below  ==============" )

#    ex_create_db( module_db_file_name )
#    ex_insert_many_test_rows( module_db_file_name )
    ex_select_all_plug_measurements( module_db_file_name )

    # old
#    print( create_table_plug_events( module_db_file_name, allow_drop = False ) )
#    print( create_table_plug_events( module_db_file_name, allow_drop = True ) )
#    ex_select_all_plug_measurements( module_db_file_name )
#    ex_select_where( module_db_file_name )

#    ex_multiply_data( module_db_file_name