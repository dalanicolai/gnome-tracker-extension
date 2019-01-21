#!/usr/bin/env python
# This script takes one filename as argument and opens a openwith gtk window 

import sys
import subprocess
import mimetypes

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class myWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Open with")
        self.set_icon_from_file(home + '/.local/share/icons/hicolor/scalable/apps/ulauncher.svg')
        
        self.connect("key-press-event", self.on_key_press)
    
    def on_key_press(self, window, event):
        print(event.keyval)
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()


def application_activated(appchooserwidget, desktopappinfo):
    app_info = appchooserwidget.get_app_info()
    exe = app_info.get_executable()
    subprocess.Popen([exe,filename])
    Gtk.main_quit() 


filename = sys.argv[1]
mime = mimetypes.guess_type(filename)[0]


window = myWindow()


window.connect("destroy", Gtk.main_quit)

appchooserwidget = Gtk.AppChooserWidget(content_type=mime)
appchooserwidget.connect("application-activated", application_activated)
window.add(appchooserwidget)


window.show_all()

Gtk.main()
