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
os.chmod(appPath + '/appchooser.py', 0o755) 


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
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
terminal_icon = icon_path('org.gnome.Terminal', 'terminal')


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

        if preferences["cb_lib_path"] == 'default':
            with open(home + '/.config/calibre/global.py') as f:
                text = f.readlines()
                for i in text:
                    if 'library_path' in i:
                        calibre_lib_path = i.strip()[17:-1]
            
        if keyword == preferences["cb_kw"]:
            import sqlite3
            if not preferences["cb_lib_path"] == 'default':
                calibre_lib_path = preferences["cb_lib_path"]
                if preferences["cb_lib_path"][-1] == '/':
                    conn = sqlite3.connect(preferences["cb_lib_path"]+"metadata.db")
                else:
                    conn = sqlite3.connect(preferences["cb_lib_path"]+"/metadata.db")
            else:
                print(calibre_lib_path+"/metadata.db")
                conn = sqlite3.connect(calibre_lib_path+"/metadata.db")
            c = conn.cursor()
            queries = query_words.split()
            
            if len(queries) == 1:
                results = c.execute('select title, author_sort, path from books where (title like "%{}%" or author_sort like "%{}%") limit 10'.format(queries[0], queries[0]))
            elif len(queries) == 2:
                results = c.execute('select title, author_sort, path from books where (title like "%{}%" or author_sort like "%{}%") and id in (select id from books where title like "%{}%" or author_sort like "%{}%")'.format(queries[1], queries[1], queries[0], queries[0]))


            items = []
            for i in results:
                cover ='images/gnome.png',
                pad = calibre_lib_path + '/{}'.format(i[2])
                for f in os.listdir(pad):
                    if f.endswith(".pdf") or f.endswith("djvu"):
                        filepath = os.path.join(pad, f)
                        print('FILE =', filepath)
                    if f.endswith(".jpg"):
                        cover = os.path.join(pad, f)
                    print("cover = ", cover)
                data = '%s' %filepath
                items.append(ExtensionResultItem(icon= '%s' %cover, 
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=ExtensionCustomAction(data, keep_app_open=True)))
            
        elif keyword == preferences["rc_kw"]:
            from recoll import recoll
            db = recoll.connect()
            query = db.query()
            query_words_list = query_words.split() 
            if not 'g' in query_words_list[:-1]:
                query.execute(query_words)
                result_list = query.fetchmany(200)
                results = [[doc.filename, query.makedocabstract(doc)[:80], doc.url] for doc in result_list[:15]]
            else:
                query.execute(' '.join(query_words_list[:query_words_list.index('g')]))
                result_list = query.fetchmany(200)
                results = [[doc.filename, query.makedocabstract(doc)[:80], doc.url] for doc in result_list if query_words_list[-1].lower() in doc.filename.lower()]
            #results = sorted(output, key=lambda entry: entry[2])[::-1]

            items = []
            for i in results:
                data = '%s' %i[2]
                items.append(ExtensionResultItem(icon='images/recoll.png',
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=ExtensionCustomAction(data, keep_app_open=True)))  
            
            
            


        elif keyword == preferences["df_kw"]:
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
                query_words_list = query_words.split() 
                if preferences["autowildcardsearch"] == 'Yes':
                    if " " in query_words: 
                        query_words = "*".join(query_words.split(' ')) + "*"
                    else:
                        if not 'g' in query_words_list[:-1]:
                            query_words = query_words
                        else:
                            query_words = ' '.join(query_words_list[:query_words_list.index('g')])
                command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) . ?f fts:match '"+query_words+"' } ORDER BY nfo:fileLastAccessed(?f)"]
#                command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) . ?f nie:plainTextContent ?w FILTER regex(?w, '"+query_words+"', 'i') }"]
                output = subprocess.check_output(command, encoding='UTF-8')
                print('HALLO', output+'\n')
                if not 'g' in query_words_list[:-1]:
                    pre_results = [i.split(', ') for i in output.splitlines()][::-1][1:-1][:20]
                else:
                    pre_results = [i.split(', ') for i in output.splitlines()[1:-1] if query_words_list[-1].lower() in i][::-1][:20]
                    print("RES",pre_results)
                results = [[pre_results[i][0][2:],pre_results[i][1][7:]] for i in range(len(pre_results))]

            elif keyword == preferences["ts_kw"]:
                import re

                out1 = subprocess.check_output(['tracker','search',query_words], encoding='UTF-8')
                out2 = [i for i in out1.splitlines()]
                out3 = [re.sub('\x1b[^m]*m', '', i).strip() for i in out2[1:]]
                pre_results = list(chunks(out3,3))[:-1]
                print(pre_results)
                results = [[pre_results[i][1],pre_results[i][0][7:]] for i in range(len(pre_results))]

            elif keyword == preferences["lc_kw"]:
                words = query_words.split(' ')
                if len(words) == 1:
                    output = subprocess.check_output(['locate','-l','11', query_words], encoding='UTF-8')
                    pre_results = output.splitlines() 
                    results = [[os.path.basename(i),i] for i in pre_results]
                elif preferences["autowildcardsearch"] == 'No':                
                    if len(words) == 3 and words[1] == 'g':
                        loc = subprocess.Popen(['locate', '-l', '100', words[0]], stdout=subprocess.PIPE)
                        #output = subprocess.run(['grep','-i', '-m','11', 'rey'], input=loc.stdout, capture_output=True)
                        output = subprocess.check_output(['grep','-i', '-m','11', words[2]], stdin=loc.stdout, encoding='UTF-8')
                        pre_results = output.splitlines() 
                        results = [[os.path.basename(i),i] for i in pre_results]
                    elif len(words) == 5 and words[1] == 'g' and words [3] == 'g':
                        loc = subprocess.Popen(['locate', '-l', '100', words[0]], stdout=subprocess.PIPE)
                        #output = subprocess.run(['grep','-i', '-m','11', 'rey'], input=loc.stdout, capture_output=True)
                        grep1 = subprocess.Popen(['grep','-i', words[2]], stdin=loc.stdout, stdout=subprocess.PIPE)
                        output = subprocess.check_output(['grep', '-i', '-m','11', words[4]], stdin=grep1.stdout, encoding='UTF-8')
                        pre_results = output.splitlines() 
                        results = [[os.path.basename(i),i] for i in pre_results]
                # Do auto wildcard search if enabled in preferences
                else:
                    output = subprocess.check_output(['locate','-i','-l','11', "*" + "*".join(words) + "*"], encoding='UTF-8')
                    pre_results = output.splitlines() 
                    results = [[os.path.basename(i),i] for i in pre_results]


            items = []
            for i in results:
                data = '%s' %i[1]
                print(data)
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
                   ['Open with file browser', extension.preferences["filebrowser"], file_browser_icon],
                   ['Open with text editor', extension.preferences["texteditor"], text_editor_icon],
                   ['Open location in {}'.format(extension.preferences["terminal"]), extension.preferences["terminal"], terminal_icon]]
        data = event.get_data().replace("%20"," ")
        items = []
        for i in options:
            if i[1] == extension.preferences["terminal"]:
                data = os.path.dirname(os.path.abspath(data))
            items.append(ExtensionResultItem(icon=i[2],
                                             name='%s' %i[0],
                                             description="%s" % data,
                                             on_enter=RunScriptAction("%s '%s'" % (i[1], data), None)))
        return RenderResultListAction(items)

if __name__ == '__main__':
    GnomeTrackerExtension().run()
