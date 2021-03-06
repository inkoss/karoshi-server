#!/bin/bash
#Copyright (C) 2014  Paul Sharrad

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

############################
#Language
############################

STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

#Check if timout should be disabled
if [ `echo $REMOTE_ADDR | grep -c $NOTIMEOUT` = 1 ]
then
TIMEOUT=86400
fi
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html>
<html>
<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>'$"Windows Printer Driver Generation"'</title><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi">
  <link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'">

  
  <script>
<!--
function SetAllCheckBoxes(FormName, FieldName, CheckValue)
{
	if(!document.forms[FormName])
		return;
	var objCheckBoxes = document.forms[FormName].elements[FieldName];
	if(!objCheckBoxes)
		return;
	var countCheckBoxes = objCheckBoxes.length;
	if(!countCheckBoxes)
		objCheckBoxes.checked = CheckValue;
	else
		// set the check value for all check boxes
		for(var i = 0; i < countCheckBoxes; i++)
			objCheckBoxes[i].checked = CheckValue;
}
// -->
  </script>
<script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'

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

echo '</head><body onLoad="start()"><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=5
#Assign action
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = ACTIONcheck ]
then
let COUNTER=$COUNTER+1
ACTION=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

#Assign queue
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = QUEUEcheck ]
then
let COUNTER=$COUNTER+1
QUEUE=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done

[ -z $ACTION ] && ACTION=view

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox3
TABLECLASS=standard
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
TABLECLASS=mobilestandard
fi

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/admin/printer_driver_gen.cgi";'
echo '</script>'
echo "</div></form></div></body></html>"
exit
}

echo '<form action="/cgi-bin/admin/printer_driver_gen.cgi" name="selectedsites" method="post"><b></b>'

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'"><div id="titlebox">'


#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Printer Driver Generation"'</span>
<a href="/cgi-bin/admin/mobile_menu.cgi">'$"Menu"'</a>
</div></div><div id="mobileactionbox">
'
fi
if [ $MOBILE = yes ]
then
echo '<table class="'$TABLECLASS'" style="text-align: left;" ><tbody>
<tr><td>
<b>'$"Windows Printer Driver Generation"'</b></td><td><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Printer_Driver_Generation"><img class="images" alt="" src="/images/help/info.png"><span>'$"This is used to enable or disable automated windows printer driver generation for your print queues."'</span></a></td></tr>
</tbody></table><br>
<input name="_ACTION_enableall_PRINTQUEUE_all_" type="submit" class="button" value="'$"Enable all"'">
<input name="_ACTION_disableall_PRINTQUEUE_all_" type="submit" class="button" value="'$"Disable all"'"><br>
<input name="_ACTION_gendrivers_PRINTQUEUE_all_" type="submit" class="button" value="'$"Generate Drivers"'"><br><br>
'
else
echo '<table class="'$TABLECLASS'" style="text-align: left;" ><tbody>
<tr>
<td style="vertical-align: top;"><b>'$"Windows Printer Driver Generation"'</b></td>
<td style="vertical-align: top;"><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Printer_Driver_Generation"><img class="images" alt="" src="/images/help/info.png"><span>'$"This is used to enable or disable automated windows printer driver generation for your print queues."'</span></a></td><td><input name="_ACTION_enableall_PRINTQUEUE_all_" type="submit" class="button" value="'$"Enable all"'"></td><td><input name="_ACTION_disableall_PRINTQUEUE_all_" type="submit" class="button" value="'$"Disable all"'"></td><td><input name="_ACTION_gendrivers_PRINTQUEUE_all_" type="submit" class="button" value="'$"Generate Drivers"'"></td></tr></table><br>
</div><div id="infobox">'
fi
MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/printer_driver_gen.cgi | cut -d' ' -f1`
if [ $ACTION = gendrivers ]
then
sudo -H /opt/karoshi/web_controls/exec/printer_driver_gen2 $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$MOBILE:
EXEC_STATUS=$?
[ $EXEC_STATUS = 0 ] && MESSAGE=$"Windows printer driver generation completed."

if [ $EXEC_STATUS = 102 ]
then
MESSAGE=$"The samba root password was incorrect."
fi
if [ $EXEC_STATUS = 103 ]
then
MESSAGE=$"The windows dll files needed to generate the windows printer drivers are missing. The dlls needed in /usr/share/cups/drivers/ are pscript5.dll, ps5ui.dll, pscript.hlp, pscript.ntf."
fi
show_status
else
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$ACTION:$QUEUE:$MOBILE:" | sudo -H /opt/karoshi/web_controls/exec/printer_driver_gen
fi
[ $MOBILE = no ] && echo '</div>'
echo '</div></form></div></body></html>'
exit
