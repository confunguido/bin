#!/usr/bin/python3
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Luke Macken <lmacken@redhat.com>
#            Miroslav Lichvar <mlichvar@redhat.com>
#            Edward Sheldrake <ejsheldrake@gmail.com>


import xdg.Menu, xdg.DesktopEntry, xdg.Config
import re, sys, os
from xml.sax.saxutils import escape

icons = True
try:
	import gi
	gi.require_version('Gtk', '3.0')
	from gi.repository import Gtk
except ImportError:
	icons = False

def icon_attr(entry):
	if icons is False:
		return ''

	name = entry.getIcon()

	if os.path.exists(name):
		return ' icon="' + name + '"'

	# work around broken .desktop files
	# unless the icon is a full path it should not have an extension
	name = re.sub('\..{3,4}$', '', name)

	# imlib2 cannot load svg
	iconinfo = theme.lookup_icon(name, 22, Gtk.IconLookupFlags.NO_SVG)
	if iconinfo:
		iconfile = iconinfo.get_filename()
		if hasattr(iconinfo, 'free'):
			iconinfo.free()
		if iconfile:
			return ' icon="' + iconfile + '"'
	return ''

def escape_utf8(s):
	if sys.version_info[0] < 3 and isinstance(s, unicode):
		s = s.encode('utf-8', 'xmlcharrefreplace')
	return escape(s)

def entry_name(entry):
	return escape_utf8(entry.getName())
def entry_exec(entry):
        return escape_utf8(entry.getExec())

def populate_menu(entry):
	if isinstance(entry, xdg.Menu.Menu) and entry.Show is True:
		list(map(populate_menu, entry.getEntries()))
	elif isinstance(entry, xdg.Menu.MenuEntry) and entry.Show is True:
                #name = entry_name(entry.DesktopEntry)
                applications_items.append(entry)

def match_entry(entry,search_str):
        return re.compile(search_str, re.IGNORECASE).match(entry_name(entry.DesktopEntry))
        
def find_matches(search_str, app_list):
        match_list = [m for m in app_list if match_entry(m,search_str)]
        return(match_list)

if len(sys.argv) > 1:
	menufile = sys.argv[1] + '.menu'
else:
	menufile = 'applications.menu'

lang = os.environ.get('LANG')
if lang:
	xdg.Config.setLocale(lang)

# lie to get the same menu as in GNOME
xdg.Config.setWindowManager('GNOME')

if icons:
  theme = Gtk.IconTheme.get_default()

menu = xdg.Menu.parse(menufile)
applications_items = list()
#print('<?xml version="1.0" encoding="UTF-8"?>')
#print('<openbox_pipe_menu>')
list(map(populate_menu, menu.getEntries()))
search_term = input('')
matches_list = list()
matches_list = find_matches(search_term.lower(), applications_items)
for m in matches_list:
        print('%s: %s' % (entry_name(m.DesktopEntry), entry_exec(m.DesktopEntry)))
#print('</openbox_pipe_menu>')