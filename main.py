import subprocess
import os
import distutils.spawn

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

home = os.getenv("HOME")
appPath = os.path.dirname(os.path.abspath(__file__))
os.chmod(appPath + '/appchooser.py', 0755) 

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]

def icon_path(*args):
    for arg in args:
        for size in [48]:
            icon = icon_theme.choose_icon([arg], size, 0)
            if icon is not None:
                return icon.get_filename()


icon_theme = Gtk.IconTheme.get_default()

file_browser_icon = icon_path('org.gnome.NautilusGtk4', 'org.gnome.Nautilus')
other_application_icon = icon_path('applications-other')
text_editor_icon = icon_path('accessories-text-editor')
terminal_icon = icon_path('terminal')


class GnomeTrackerExtension(Extension):

    def __init__(self):
        super(GnomeTrackerExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        
        keyword = event.get_keyword()
        preferences = extension.preferences
        query_words = event.get_argument()
        if query_words == None:
            query_words = ""

        if keyword == preferences["df_kw"]:
            from search import search
            out = search(query_words,28834)
            output = [[doc.getFilename(),doc.getPathStr(),doc.getLastModifiedStr()] for doc in out]
            results = sorted(output, key=lambda entry: entry[2])[::-1]

            items = []
            for i in results:
                data = '%s' %i[1]
                items.append(ExtensionResultItem(icon='images/docfetcher.png',
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=ExtensionCustomAction(data, keep_app_open=True)))     
        
        else:
            if keyword == preferences["gt_kw"]:
                if " " in query_words: 
                    query_words = "*".join(query_words.split(' ')) + "*"
                else:
                    query_words = query_words + "*"
                command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) . ?f fts:match '"+query_words+"' } ORDER BY nfo:fileLastAccessed(?f)"]
                output = subprocess.check_output(command)          
                pre_results = [i.split(', ') for i in output.splitlines()][::-1][1:-1][:20]
                results = [[pre_results[i][0][2:],pre_results[i][1][7:]] for i in range(len(pre_results))]

            elif keyword == preferences["ts_kw"]:
                import re

                out1 = subprocess.check_output(['tracker','search',query_words])
                out2 = [i for i in out1.splitlines()]
                out3 = [re.sub('\x1b[^m]*m', '', i).strip() for i in out2[1:]]
                pre_results = list(chunks(out3,3))[:-1]
                print(pre_results)
                results = [[pre_results[i][1],pre_results[i][0][7:]] for i in range(len(pre_results))]

            elif keyword == preferences["lc_kw"]:
                words = query_words.split(' ')
                if len(words) == 1:
                    output = subprocess.check_output(['locate','-l','11', query_words])
                    pre_results = output.splitlines() 
                    results = [[os.path.basename(i),i] for i in pre_results]
                elif len(words) == 3 and words[1] == 'g':
                    loc = subprocess.Popen(('locate', words[0]), stdout=subprocess.PIPE)
                    output = subprocess.check_output(('grep','-m','11', words[2]), stdin=loc.stdout)
                    pre_results = output.splitlines() 
                    results = [[os.path.basename(i),i] for i in pre_results]
                elif len(words) == 5 and words[1] == 'g' and words [3] == 'g':
                    loc = subprocess.Popen(('locate', words[0]), stdout=subprocess.PIPE)
                    grep1 = subprocess.Popen(('grep', words[2]),stdin=loc.stdout, stdout=subprocess.PIPE)
                    output = subprocess.check_output(('grep','-m','11', words[4]), stdin=grep1.stdout)
                    print(output)
                    pre_results = output.splitlines() 
                    results = [[os.path.basename(i),i] for i in pre_results]

            items = []
            for i in results:
                data = '%s' %i[1]
                items.append(ExtensionResultItem(icon='images/gnome.png',
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=ExtensionCustomAction(data, keep_app_open=True)))
        return RenderResultListAction(items)

class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        appchooser_path = appPath + '/appchooser.py'
        options = [['Open with default application', 'xdg-open','images/detective_penguin.png'],
                   ['Open with other application', appchooser_path, other_application_icon],
                   ['Open with file browser', 'nautilus', file_browser_icon],
                   ['Open with text editor', 'gedit', text_editor_icon],
                   ['Open location in terminal', 'gnome-terminal --working-directory', terminal_icon]]
        data = event.get_data().replace("%20"," ")
        items = []
        for i in options:
            if i[2] == 'terminal':
                data = os.path.dirname(os.path.abspath(data))
            items.append(ExtensionResultItem(icon=i[2],
                                             name='%s' %i[0],
                                             description="%s" % data,
                                             on_enter=RunScriptAction("%s '%s'" % (i[1], data), None)))
        return RenderResultListAction(items)

if __name__ == '__main__':
    GnomeTrackerExtension().run()
