#!/bin/bash
#Copyright (C) 2008  Paul Sharrad

#This file is part of Karoshi Server.
#
#Karoshi Server is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Karoshi Server is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.
#
#You should have received a copy of the GNU Affero General Public License
#along with Karoshi Server.  If not, see <http://www.gnu.org/licenses/>.

#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

########################
#Required input variables
########################
#  _USERNAME_
#  _SURNAME_
# _DAY_
# _MONTH_
# _YEAR_
##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"User Internet Logs"'</title><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"><script src="/all/stuHover.js" type="text/javascript"></script>
<script src="/all/js/jquery.js"></script>
<script src="/all/js/jquery.tablesorter/jquery.tablesorter.js"></script>
<script id="js">
$(document).ready(function() 
    { 
        $("#myTable").tablesorter({
	headers: {
	0: { sorter: false},
	2: { sorter: false},
	3: { sorter: "ipAddress" },
	4: { sorter: false}
    		}
		});
    } 
);
</script>
<meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: www.dynamicdrive.com
		* Visit Dynamic Drive at www.dynamicdrive.com for full source code
		***********************************************/
	</script>
	<script>
	// <![CDATA[
	var myMenu;
	window.onload = function() {
		myMenu = new SDMenu("my_menu");
		myMenu.init();
	};
	// ]]>
	</script>'
fi

echo '</head><body><div id="pagecontainer">'

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox3
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
fi

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'"><div id="titlebox">'

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=14
#Assign USERNAME
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = USERNAMEcheck ]
	then
		let COUNTER=$COUNTER+1
		USERNAME=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done
#Assign DATE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = DATEcheck ]
	then
		let COUNTER=$COUNTER+1
		DATE=`echo $DATA | cut -s -d'_' -f$COUNTER | tr -cd '0-9-'`
		break
	fi
	let COUNTER=$COUNTER+1
done

#Assign DAYCOUNT
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = DAYCOUNTcheck ]
	then
		let COUNTER=$COUNTER+1
		DAYCOUNT=`echo $DATA | cut -s -d'_' -f$COUNTER | tr -cd '0-9-'`
		break
	fi
	let COUNTER=$COUNTER+1
done

#Assign DETAILED
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = DETAILEDcheck ]
	then
		let COUNTER=$COUNTER+1
		DETAILED=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/dg_view_user_logs_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}
#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
	export MESSAGE=$"You must access this page via https."
	show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi
#########################
#Check data
#########################
#Check to see that USERNAME is not blank
if [ -z "$USERNAME" ]
then
	MESSAGE=$"The username cannot be blank."
	show_status
fi

DAY=`echo $DATE | cut -d- -f1`
MONTH=`echo $DATE | cut -d- -f2`
YEAR=`echo $DATE | cut -d- -f3`

#Check to see that DAYCOUNT is not blank
if [ -z "$DAYCOUNT" ]
then
	DAYCOUNT=1
fi

#Check to see that DETAILED is not blank
if [ -z "$DETAILED" ]
then
	DETAILED=no
else
	#Check that DETAILED is yes
	if [ $DETAILED != yes ] && [ $DETAILED != no ]
	then
		MESSAGE=$"Incorrect detail value."
		show_status
	fi
fi

#Check that DAYCOUNT is not greater than 99
if [ $DAYCOUNT -gt 99 ]
then
	MESSAGE=$"Your username or password was not correct."
	show_status
fi

#Loop round for the number of days to check the log for
COUNTER=1
while [ $COUNTER -le $DAYCOUNT ]
do
	#Check to see that DATE is not blank
	if [ -z "$DATE" ]
	then
		MESSAGE=$"The date cannot be blank."
		show_status
	fi

	#Check to see that DAY is not blank
	if [ -z "$DAY" ]
	then
		MESSAGE=$"The date cannot be blank."
		show_status
	fi

	#Check to see that MONTH is not blank
	if [ -z "$MONTH" ]
	then
		MESSAGE=$"The date cannot be blank."
		show_status
	fi

	#Check to see that YEAR is not blank
	if [ -z "$YEAR" ]
	then
		MESSAGE=$"The date cannot be blank."
		show_status
	fi

	#Check that day is not greater than 31
	if [ $DAY -gt 31 ]
	then
		MESSAGE=$"Date input error."
		show_status
	fi

	#Check that the month is not greater than 12
	if [ $MONTH -gt 12 ]
	then
		MESSAGE=$"Date input error."
		show_status
	fi

	if [ $YEAR -lt 2006 ] || [ $YEAR -gt 3006 ]
	then
		MESSAGE=$"The year is not valid."
		show_status
	fi

	#Show back button for mobiles
	if [ $MOBILE = yes ]
	then
	echo '<div style="float: center" id="my_menu" class="sdmenu">
		<div class="expanded">
		<span>'$"User Internet Logs"'</span>
	<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Menu"'</a>
	</div></div><div id="mobilecontent"><div id="mobileactionbox2">
	'
	fi

	MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/dg_view_user_logs.cgi | cut -d' ' -f1`
	#View logs
	echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$USERNAME:$DAY:$MONTH:$YEAR:$DETAILED:$MOBILE:" | sudo -H /opt/karoshi/web_controls/exec/dg_view_user_logs
	EXEC_STATUS=`echo $?`
	if [ $EXEC_STATUS = 101 ]
	then
		MESSAGE=`echo $"There was a problem with this action." $"Internet Logs for"`
		show_status
	fi
	if [ $EXEC_STATUS = 102 ]
	then
		echo ''$DAY-$MONTH-$YEAR - $USERNAME'<br><br>'$"No log for this date."'<br>'
	fi
	# Add one to the day
	DATE=`date +%F -d "$YEAR-$MONTH-$DAY 1 days"`

	DAY=`echo $DATE | cut -d- -f3`
	MONTH=`echo $DATE | cut -d- -f2`
	YEAR=`echo $DATE | cut -d- -f1`

	let COUNTER=$COUNTER+1
done

echo '</div></div></div></body></html>'
exit
