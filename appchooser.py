#!/usr/bin/env python
# This script takes one filename as argument and opens a openwith gtk window 

import sys
import subprocess
import mimetypes

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


def application_activated(appchooserwidget, desktopappinfo):
    app_info = appchooserwidget.get_app_info()
    exe = app_info.get_executable()
    subprocess.Popen([exe,filename])
    Gtk.main_quit()
    
filename = sys.argv[1]
mime = mimetypes.guess_type(filename)[0]


window = Gtk.Window()
window.set_title("open with")
window.connect("destroy", lambda q: Gtk.main_quit())

appchooserwidget = Gtk.AppChooserWidget(content_type=mime)
appchooserwidget.connect("application-activated", application_activated)
window.add(appchooserwidget)

window.show_all()

Gtk.main()
