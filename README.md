Purpose: This is a pair of Graphical User Interface Application is to control TP-LINK HS110 Smart Plug w/Energy Monitoring ( TP-LINK HS110 Smart Plug w/Energy Monitoring - - Amazon.com ) and other TP link devices, it works with simpler smart plugs and perhaps other devices.  It will also graph and otherwise process the data. The application uses the pyHS100 library code.  

* Program One: smart_plug.py - Monitors, controls, collects ( to memory and database ), and graphs data from smart plugs.
* Program Two: smart_plug_graph.py - Pulls smartplug data from the database to graph or convert to csv.

Enviroment: 
* Program should run on any OS supporting Python 3.6.  
* This should include Windows, Mac, Linux, and Raspberry Pi, but currently the matplotlib has fatal issues on all but windows.
* So far only tested on 
** Windows 
** More coming... perhaps. ( I do not have a mac ) 

Program Status: Back to alpha ( maybe even beta ). 

Docs are a bit out of date.  I plan to fix than and then put this app on a shelf for awhile. Intended for those with some Python experience who can add the files to their Python development environment ( no install features for this code ). Some dependencies will need to be installed, probably prompted by error messages. Editing of the parameter file should be easier for those with Python experience. Users should find some useful documentation in the code, this is still a work in progress. Much code has been lifted from other projects of mine, some artifacts of the other projects remain.

http://www.opencircuits.com/Python_Control_of_Smart_Plugs


``` 
	Standard Disclaimer:
		If you have more than a casual interest in this project you should contact me 
		( no_spam_please_666 at comcast.net ) and see if the repository is actually in good shape.  
		I may well have improved software and or documentation.  
		I will try to answer all questions and perhaps even clean up what already exists.	
``` 		

Would You Like to Contribute??
* Add other iot devices/sensors.
* Link to cloud.
* Support other databases.
* Other ideas.
* Bug reports -- which I will read and may fix.
	
```	
	Note for contributers 
		Fixes would be great.
		Extensions would be great.
		Re write of current code would generally be discouraged... but you are free to create a fork of your own.
		( take a look at readme_rsh.txt for some additional notes on changes... )
	
```
Guide to Repository

* Root - all code ( src ) required to run the application.  I think it qualifies as pure python ( 3.6 ).  See introduction here for the files containing the "main programs".
* images - various graphics: screen shots, and extra icons....
* wiki_etc - pdf versions of the wiki at open circuits.
