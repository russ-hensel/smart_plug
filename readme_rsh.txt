this file should be: D:\Russ\0000\python00\python3\_projects\smart_plug\Ver6\readme_rsh.txt


status:   working -- but many parts and features are being added or moved around, testing minimal


================ current work and ideas ==================

** get an icon for gui -- have icons may want to improve
*! add current value labels to gui  added watts enough??
** add live graph -- for one or many refresh rate
** add units to timer
!!
!! energy may be kilo watt hr, check device then fix graph and csv
!! file open, lock, change create issues sort of open
** add a mode like record, but just monitor -- only for energy plugs, which is now what we assume
!! us my data filter functions for datapoint....
** get grid on graph
!! graph with mixed units days, hrs.... if not for this just to learn how
** live graph
!! live graph to csv
!! live graph to db
!! consider purpose and location as plug attributes
!! constrain actions for plugs that are not present or do not monitor energy

!! when timer times out need to uncheck the on checkbox
!! Retrieve energy data from plug: On the GUI, but not implemented.
!! move probe into helper thread, have a stop for it
!! seperate log files for two apps
!! why 5 lines when graphing 2 devices
!!

!!    self.show_db_updates      = True   # show updates in message area
!! smartplug .... auto scroll on off seems not to work correctly
!! probably take total energy off
** time from now
!! more memory reports
** convert to numpy




=============== graph live ================

!! need y axis label -- with units



=============== graph db ====================


!! get device id of some sort on the ledgend
!! energy graph seems off
!! add ways to set the time interval like to today, now minus 1 hr.....
so the radio buttons for select
!!fix alignment.....

-- time range set:
** today from parameters/ last hr/ others....
!! this week / this month

!! may be all i need, can use radio button then change
!! name the csv file in message

--------------------------- scratch --------------

total_power     total_energy


------------------------- gui notes   --------------------








================== old code, reference for awhile =================================



plt.legend([plot1,plot2],["plot 1", "plot 2"])


se handles AKA Proxy artists

import matplotlib.lines as mlines
import matplotlib.pyplot as plt
# defining legend style and data
blue_line = mlines.Line2D([], [], color='blue', label='My Label')
reds_line = mlines.Line2D([], [], color='red', label='My Othes')

plt.legend(handles=[blue_line, reds_line])

plt.show()


plt.legend([plot1,plot2],["plot 1", "plot 2"])

AttributeError: 'SmartPlugAdapter' object has no attribute 'end_graph_live'
No handles with labels found to put in legend.












