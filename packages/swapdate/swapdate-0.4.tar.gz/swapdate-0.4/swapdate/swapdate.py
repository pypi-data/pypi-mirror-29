#!usr/bin/python

########################################################################################################
# Module Name: swapdate.py
# Author     : Vijaylingam.
# CreatedDate: 12/10/2016.
# Description: Library to convert and get different format of date & time
# Input Parameter : Format
# Output Parameter: Formatted date or Formatted time or Formatted date time
# Change History	 :
# Date    Programmer 	 Description
# ----	  ---------- 	 -----------
#	12/10/2016	| Vijaylingam		|	Initial Code
#				|					|			
########################################################################################################

#####################################
# Available Formats
#####################################

# Days 		(D) 	-- 173 (Julian)
# European 	(E) 	-- 22/06/16
# European 	(EX) 	-- 22/06/2016
# Month 	(M) 	-- Jun
# Month 	(MX) 	-- June
# Normal 	(N) 	-- 22 Jun 2002
# Normal 	(NX) 	-- 22 June 2002
# Ordered 	(O) 	-- 16/06/22
# Ordered 	(OX) 	-- 2016/06/22
# Standard 	(S) 	-- 160622
# Standard 	(SX) 	-- 20160622
# USA 		(U) 	-- 06/22/16
# USA 		(UX) 	-- 06/22/2016
# Weekday 	(W) 	-- Sat
# Weekday 	(WX) 	-- Saturday
# Time 		(T12) 	-- 01:56 PM
# Time 		(T12X) 	-- 01:56:00 PM
# Time 		(T12XX) -- 01:56:00:000000 PM
# Time 		(T24) 	-- 13:56 PM
# Time 		(T24X) 	-- 13:56:00 PM
# Time 		(T24XX) -- 13:56:00:000000 PM
# Default			-- 03/23/16 14:23:56



import time
from datetime import datetime,timedelta

def get(format=""):
	format = format.upper()
	date = datetime.now()
	if format == "U":
		return str(date.strftime('%m/%d/%y'))
		
	if format == "UX":
		return str(date.strftime('%m/%d/%Y'))
		
	elif format == "S":
		return str(date.strftime('%y%m%d'))
		
	elif format == "SX":
		return str(date.strftime('%Y%m%d'))
		
	elif format == "W":
		return str(date.strftime('%a'))
		
	elif format == "WX":
		return str(date.strftime('%A'))
		
	elif format == "O":
		return str(date.strftime('%y/%m/%d'))

	elif format == "OX":
		return str(date.strftime('%Y/%m/%d'))
		
	elif format == "M":
		return str(date.strftime('%b'))
		
	elif format == "MX":
		return str(date.strftime('%B'))
		
	elif format == "E":
		return str(date.strftime('%d/%m/%y'))
		
	elif format == "EX":
		return str(date.strftime('%d/%m/%Y'))
		
	elif format == "T12":
		return str(date.strftime('%I:%M %p'))
		
	elif format == "T12X":
		return str(date.strftime('%I:%M:%S %p'))
		
	elif format == "T12XX":
		return str(date.strftime('%I:%M:%S:%f %p'))
		
	elif format == "T24X":
		return str(date.strftime('%H:%M:%S %p'))
		
	elif format == "T24XX":
		return str(date.strftime('%H:%M:%S:%f %p'))
		
	elif format == "T24":
		return str(date.strftime('%H:%M %p'))
		
	elif format == "N":
		return str(date.strftime('%d %b %Y'))
		
	elif format == "NX":
		return str(date.strftime('%d %B %Y'))
		
	elif format == "D":
		return str(date.strftime('%j'))
		
	elif format == "":
			return str(date.strftime('%m/%d/%y %H:%M:%S'))
			
	else:
		return None