#!/bin/bash
#Copyright (C) 2011  Paul Sharrad
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
#jharris@karoshi.org.uk
#aball@karoshi.org.uk
#
#Website: http://www.karoshi.org.uk

##########################
#Language
##########################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printer_accounting ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/printer/printer_accounting
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all


#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
END_POINT=7
#Assign LOGTYPE
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = LOGTYPEcheck ]
then
let COUNTER=$COUNTER+1
LOGTYPE=`echo $DATA | cut -s -d'_' -f$COUNTER`
break
fi
let COUNTER=$COUNTER+1
done


##########################
#Show page
##########################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE9'</title><link rel="stylesheet" href="/css/'$STYLESHEET'"><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480--></head><body>'


function show_status {
echo '<script type="text/javascript">'
echo 'alert("'$MESSAGE'");'
echo 'window.location = "/cgi-bin/admin/printer_accounting_view_logs_fm.cgi";'
echo '</script>'
echo "</div></body></html>"
exit
}

#########################
#Check https access
#########################
if [ https_$HTTPS != https_on ]
then
export MESSAGE=$HTTPS_ERROR
show_status
fi
#########################
#Check user accessing this script
#########################
if [ ! -f /opt/karoshi/web_controls/web_access_admin ] || [ $REMOTE_USER'null' = null ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi

if [ `grep -c ^$REMOTE_USER: /opt/karoshi/web_controls/web_access_admin` != 1 ]
then
MESSAGE=$ACCESS_ERROR1
show_status
fi
#########################
#Check data
#########################
#Check to see that LOGTYPE is not blank
if [ $LOGTYPE'null' = null ]
then
MESSAGE=$ERRORMSG7
show_status
fi


#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=menubox
fi
echo '<div id="'$DIV_ID'">'
echo '<b>'$TITLE9'</b><br><br>'
MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/printer_accounting_view_logs.cgi | cut -d' ' -f1`
#View printer logs
echo "$REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$LOGTYPE:" | sudo -H /opt/karoshi/web_controls/exec/printer_accounting_view_logs
echo '</div></body></html>'
exit
