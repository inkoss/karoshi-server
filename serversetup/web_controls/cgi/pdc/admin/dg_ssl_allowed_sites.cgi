#!/bin/bash
#Copyright (C) 2011 Paul Sharrad

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
########################
#Required input variables
########################
#  _WEBADDRESS_
#  _FILTERGROUP_  staff and students
############################
#Language
############################

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
TEXTDOMAIN=karoshi-server

############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$"Allow SSL Internet Sites"'</title><link rel="stylesheet" href="/css/'$STYLESHEET'?d='`date +%F`'"></head><body><div id="pagecontainer">'
#########################
#Get data input
#########################
TCPIP_ADDR=$REMOTE_ADDR
DATA=`cat | tr -cd 'A-Za-z0-9\._:%/-'`
#########################
#Assign data to variables
#########################
END_POINT=6
#Assign WEBADDRESS
COUNTER=2
while [ $COUNTER -le $END_POINT ]
do
DATAHEADER=`echo $DATA | cut -s -d'_' -f$COUNTER`
if [ `echo $DATAHEADER'check'` = WEBADDRESScheck ]
then
let COUNTER=$COUNTER+1
WEBADDRESS=`echo $DATA | cut -s -d'_' -f$COUNTER | tr 'A-Z' 'a-z' | sed 's/^http//g'`
WEBADDRESS=`echo $WEBADDRESS | sed 's/%3a//g' | sed 's/%2f//g'`
WEBADDRESS=`echo $WEBADDRESS | sed 's/^www.//g'`
WEBADDRESS=`echo $WEBADDRESS | tr -cd 'A-Za-z0-9\._/-'`
break
fi
let COUNTER=$COUNTER+1
done

function show_status {
echo '<SCRIPT language="Javascript">'
echo 'alert("'$MESSAGE'")';
echo 'window.location = "dg_ssl_allowed_sites_fm.cgi"'
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
#Check to see that WEBADDRESS is not blank
if [ $WEBADDRESS'null' = null ]
then
MESSAGE=$"You have not entered in a web address."
show_status
fi

#Check to see that the address is a full address
if [ `echo $WEBADDRESS | grep -c -F .` = 0 ]
then
MESSAGE=$"Please enter the full address without http://www or subdirectories."
show_status
fi

MD5SUM=`md5sum /var/www/cgi-bin_karoshi/admin/dg_ssl_allowed_sites.cgi | cut -d' ' -f1`
sudo -H /opt/karoshi/web_controls/exec/dg_ssl_allowed_sites $REMOTE_USER:$REMOTE_ADDR:$MD5SUM:$WEBADDRESS:
MESSAGE=`echo $WEBADDRESS $"The site has been added."`
show_status
exit

