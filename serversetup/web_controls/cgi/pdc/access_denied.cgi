#!/bin/bash
#Copyright (C) 2007  Paul Sharrad
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

STYLESHEET=defaultstyle.css
[ -f /opt/karoshi/web_controls/global_prefs ] && source /opt/karoshi/web_controls/global_prefs
source /opt/karoshi/web_controls/version
############################
#Show page
############################
echo "Content-type: text/html"
echo ""
echo '
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type">
<META HTTP-EQUIV="refresh" CONTENT="300; URL=/cgi-bin/blank.cgi">
  <title>'$"Access Denied"'</title>
<link href="/css/'$STYLESHEET'" rel="stylesheet" type="text/css">
</head>
<body><div id="pagecontainer"><div id="header">'


echo '<img src="/images/small_logo.png" alt="logo" align="top"> <font style="font-weight: bold;" size="+2">Web Management '$SCHOOL_NAME'</font> <small><small>
'$VERSIONMSG' : '$VERSION'
</small></small>
'

echo '</div><div id="navbar"><span class="preload1"></span>
<span class="preload2"></span>

<ul id="nav">
	<li class="top"><a href="/cgi-bin/menu.cgi" class="top_link"><span>Home</span></a></li>
</ul></div>
'

echo '<div id="actionbox">
<b>'$ERRORMSG 401 - $"Authentication required"'</b><br><br>
'$"You are not allowed to view this page until you have supplied a correct username and password."'<br>
</div></div>
</body>
</html>
'
exit

