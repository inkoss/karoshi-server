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
############################
#Language
############################
LANGCHOICE=englishuk
STYLESHEET=defaultstyle.css
TIMEOUT=300
NOTIMEOUT=127.0.0.1
[ -f /opt/karoshi/web_controls/user_prefs/$REMOTE_USER ] && source /opt/karoshi/web_controls/user_prefs/$REMOTE_USER
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/file/federated_file_sync ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/file/federated_file_sync
[ -f /opt/karoshi/web_controls/language/$LANGCHOICE/all ] || LANGCHOICE=englishuk
source /opt/karoshi/web_controls/language/$LANGCHOICE/all
source /opt/karoshi/serversetup/variables/years
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>'$TITLE'</title><META HTTP-EQUIV="CACHE-CONTROL" CONTENT="NO-CACHE"><meta http-equiv="REFRESH" content="'$TIMEOUT'; URL=/cgi-bin/admin/logout.cgi"><link rel="stylesheet" href="/css/'$STYLESHEET'"><script src="/all/stuHover.js" type="text/javascript"></script><meta name="viewport" content="width=device-width, initial-scale=1"> <!--480-->
</head>
<body>'
#########################
#Get data input
#########################
DATA=`cat | tr -cd 'A-Za-z0-9\._:\-'`
#########################
#Assign data to variables
#########################
FILE=`echo $DATA | cut -s -d_ -f7`

#Detect mobile browser
MOBILE=no
source /opt/karoshi/web_controls/detect_mobile_browser

#Generate navigation bar
if [ $MOBILE = no ]
then
DIV_ID=actionbox
WIDTH=150
MAXCOLS=4
#Generate navigation bar
/opt/karoshi/web_controls/generate_navbar_admin
else
DIV_ID=actionbox2
WIDTH=90
MAXCOLS=2
fi
echo '<form name="myform" action="/cgi-bin/admin/federated_file_sync.cgi" method="post"><div id="'$DIV_ID'">'

#Show back button for mobiles
if [ $MOBILE = yes ]
then
echo '<table class="standard" style="text-align: left;" border="0" cellpadding="0" cellspacing="0">
<tbody><tr><td style="vertical-align: top;"><a href="/cgi-bin/admin/mobile_menu.cgi"><img border="0" src="/images/submenus/mobile/back.png" alt="'$BACKMSG'"></a></td>
<td style="vertical-align: middle;"><a href="/cgi-bin/admin/mobile_menu.cgi"><b>'$TITLE'</b></a></td></tr></tbody></table>'
else
echo '<b>'$TITLE'</b> <a class="info" href="javascript:void(0)"><img class="images" alt="" src="/images/help/info.png"><span>'$HELPMSG1'</span></a><br><br>'
fi

#Check that this server is a federated server
if [ ! -d  /opt/karoshi/server_network/federated_ldap_servers ]
then
echo $ERRORMSG1 '</div></body></html>'
exit
fi

if [ `ls -1 /opt/karoshi/server_network/federated_ldap_servers | wc -l` = 0 ]
then
echo $ERRORMSG1 '</div></body></html>'
exit
fi

#Show list groups to enable file sync between federated servers.


echo '<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'


#Show all primary groups
COLCOUNT=1
for PGROUPS in /opt/karoshi/server_network/group_information/*
do
PGROUP=`basename $PGROUPS`
if [ -f /opt/karoshi/server_network/group_information/$PGROUP ]
then

ICON=/images/submenus/user/nosync.png
ACTION=sync
MESSAGE="$PGROUP - $ENABLESYNCMSG"
if [ -f /opt/karoshi/server_network/federated_file_sync/$PGROUP ]
then
ACTION=nosync
ICON=/images/submenus/user/sync.png
MESSAGE="$PGROUP - $DISABLESYNCMSG"
fi
echo '<td><a class="info" href="javascript:void(0)"><input name="___GROUP___'$PGROUP'___ACTION___'$ACTION'___" type="image" class="images" src="'$ICON'" value=""><span>'$MESSAGE'</span></a></td><td style="width: '$WIDTH'px;">'$PGROUP'</td>'
let COLCOUNT=$COLCOUNT+1
if [ $COLCOUNT -gt $MAXCOLS ]
then
echo "</tr><tr>"
COLCOUNT=1
fi
fi
done

echo '</tbody></table><br><br><b>'$CUSTOMFOLDERSMSG'</b><br><br>'

#Show list of custom folders to sync
if [ -d /opt/karoshi/server_network/federated_file_sync_custom ]
then
if [ `ls -1 /opt/karoshi/server_network/federated_file_sync_custom | wc -l` -gt 0 ]
then
COLCOUNT=1
ICON=/images/submenus/user/sync.png
echo '<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody><tr>'
for CUSTOMFOLDERS in /opt/karoshi/server_network/federated_file_sync_custom/*
do
CUSTOMFOLDER=`basename "$CUSTOMFOLDERS"`
echo '<td><a class="info" href="javascript:void(0)"><input name="___GROUP___'$CUSTOMFOLDER'___ACTION___customdelete___" type="image" class="images" src="'$ICON'" value=""><span>'$CUSTOMFOLDER' - '$DISABLESYNCMSG'</span></a></td><td style="width: '$WIDTH'px;">'$CUSTOMFOLDER'</td>'
let COLCOUNT=$COLCOUNT+1
if [ $COLCOUNT -gt $MAXCOLS ]
then
echo "</tr><tr>"
COLCOUNT=1
fi
done
echo '</tbody></table><br><br>'
fi
fi

#Show choice of extra folders that can be synchronised
echo '<table class="standard" style="text-align: left;" border="0" cellpadding="2" cellspacing="2"><tbody>
<tr><td style="width: 180px;">Add folder</td><td><select name="___ACTION___customadd___">'
for FOLDERCHOICES in /home/*
do
#There must be a better way than this to get round the problem of basename handling spaces!
FOLDERCHOICES=`echo "$FOLDERCHOICES" | sed 's/ /THISISASPACE/g'`
FOLDERCHOICE=`basename $FOLDERCHOICES`
FOLDERCHOICE=`echo $FOLDERCHOICE | sed 's/THISISASPACE/ /g'`
if [ -d /home/"$FOLDERCHOICE" ]
then
if [ `echo $FOLDERCHOICE | tr -cd 'A-Za-z0-9\._:\-' | sed 's/ //g'` != users ]
then
if [ ! -f /opt/karoshi/server_network/federated_file_sync_custom/"$FOLDERCHOICE" ]
then
echo '<option value="___GROUP___'$FOLDERCHOICE'">'$FOLDERCHOICE'</option>'
fi
fi
fi
done
echo '</select></td><td><input value="'$SUBMITMSG'" type="submit"></td></tr></tbody></table>'

echo '</div></form></body></html>'
exit

