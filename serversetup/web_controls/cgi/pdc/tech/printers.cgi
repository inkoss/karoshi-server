#!/bin/bash
#Copyright (C) 2007 Paul Sharrad
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#The Karoshi Team can be contacted at: 
#mpsharrad@karoshi.org.uk
#jsharrad@karoshi.org.uk

#
#Website: http://www.karoshi.org.uk

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

##########################
#Language
##########################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

##########################
#Show page
##########################
function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo '                window.location = "/cgi-bin/tech/printers_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Manage Print Queues"'</title><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"><META HTTP-EQUIV="refresh" CONTENT="60"><script src="/all/stuHover.js" type="text/javascript"></script>
<script type="text/javascript" src="/all/js/jquery.js"></script>
<script type="text/javascript" src="/all/js/jquery.tablesorter/jquery.tablesorter.js"></script>
<script type="text/javascript" id="js">
$(document).ready(function() 
    { 
        $("#myTable").tablesorter(); 
    } 
);
</script>
<meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->'
if [ $MOBILE = yes ]
then
echo '<link rel="stylesheet" type="text/css" href="/all/mobile_menu/sdmenu.css">
	<script type="text/javascript" src="/all/mobile_menu/sdmenu.js">
		/***********************************************
		* Slashdot Menu script- By DimX
		* Submitted to Dynamic Drive DHTML code library: http://www.dynamicdrive.com
		* Visit Dynamic Drive at http://www.dynamicdrive.com/ for full source code
		***********************************************/
	</script>
	<script type="text/javascript">
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

#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=2
#Assign PRINTER
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
	DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
	if [ `echo $DATAHEADER'check'` = PRINTERcheck ]
	then
		let COUNTER=$COUNTER+1
		PRINTER=`echo $DATA | cut -s -d'_' -f$COUNTER`
		break
	fi
	let COUNTER=$COUNTER+1
done

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
if [ ! -f /opt/karoshi/web_controls/web_access_tech ] || [ $REMOTE_USER'null' = null ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_tech` != 1 ]
then
	MESSAGE=$"You must be a Karoshi Management User to complete this action."
	show_status
fi

#Generate navigation bar
if [ $MOBILE = no ]
then
	DIV_ID=actionbox3
	#Generate navigation bar
	/opt/karoshi/web_controls/generate_navbar_tech
else
	DIV_ID=actionbox2
fi

#Check that a print server has been declared
function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$"A print server has not yet been set up."'")';
echo 'window.location = "karoshi_servers_view.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}

[ ! -f /opt/karoshi/server_network/printserver ] && show_status

[ $MOBILE = no ] && echo '<div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
	echo '<div style="float: center" id="my_menu" class="sdmenu">
	<div class="expanded">
	<span>'$"Manage Print Queues"'</span>'
	if [ -z "$PRINTER" ]
	then
		echo '<a href="/cgi-bin/tech/mobile_menu.cgi">'$"Menu"'</a>'
	else
		echo '<a href="/cgi-bin/tech/printers.cgi">'$"View Print Queues"'</a>'
	fi
	echo '</div></div>'
else
	echo '<div id="titlebox"><table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody>
<tr><td style="vertical-align: top; height:30px"><b>'$"Manage Print Queues"'</b></td>
<td style="vertical-align: top;"><a class="info" target="_blank" href="http://www.linuxschools.com/karoshi/documentation/wiki/index.php?title=Manage_Print_Queues"><img class="images" alt="" src="/images/help/info.png"><span>'$"Click on the icons to control the printers in each queue."'</span></a></td>'

	if [ ! -z "$PRINTER" ]
	then
		echo '<td style="vertical-align: top;"><a href="printers.cgi"><input class="button" type="button" name="" value="'$"View Print Queues"'"></a></td>'
	fi

 echo '</tr></tbody></table></div><div id="infobox">
'
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/tech/printers.cgi | cut -d' ' -f1`
sudo -H /opt/karoshi/web_controls/exec/printers $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$MOBILE:$PRINTER:
[ $MOBILE = no ] && echo '</div>'
echo '</div></div></body></html>'
exit
