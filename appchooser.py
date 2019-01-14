#!/usr/bin/env python3

import sys
import subprocess
import mimetypes

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import notify2

def application_activated(appchooserwidget, desktopappinfo):
    app_info = appchooserwidget.get_app_info()
    exe = app_info.get_executable()
    subprocess.Popen([exe,filename])
    Gtk.main_quit()
    
filename = sys.argv[1]
mime = mimetypes.guess_type(filename)[0]

### uncomment send notification with filename = sys.argv[1] for debugging purposes

# notify2.init('appchooser')
# n = notify2.Notification("Open file",
#                         filename,
#                         "notification-message-im"   # Icon name
#                        )
# n.show()

window = Gtk.Window()
window.set_title("open with")
window.connect("destroy", lambda q: Gtk.main_quit())

appchooserwidget = Gtk.AppChooserWidget(content_type=mime)
appchooserwidget.connect("application-activated", application_activated)
window.add(appchooserwidget)

window.show_all()

Gtk.main()
