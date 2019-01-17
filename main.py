import subprocess
import os
import distutils.spawn

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction

yad_path = distutils.spawn.find_executable('yad')

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


class GnomeTrackerExtension(Extension):

    def __init__(self):
        super(GnomeTrackerExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
		
        keyword = event.get_keyword()
        query_words = event.get_argument()
        if query_words == None:
            query_words = ""
        home = os.getenv("HOME")

        if keyword == 'df':
            print('wat is dit', event.get_keyword())
            from search import search
            out = search(query_words,28834)
            output = [[doc.getFilename(),doc.getPathStr(),doc.getLastModifiedStr()] for doc in out]
            results = sorted(output, key=lambda entry: entry[2])[::-1]

            items = []
            for i in results:
                items.append(ExtensionResultItem(icon='images/docfetcher.png',
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=RunScriptAction("~/.cache/ulauncher_cache/extensions/com.github.dalanicolai.gnome-tracker-extension/ulaction '%s'" %i[1].replace("%20"," "), None)))      
        
        else:
            if keyword == 'gt':
                command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) . ?f fts:match '"+query_words+"' } ORDER BY nfo:fileLastAccessed(?f)"]
                output = subprocess.check_output(command)          
                pre_results = [i.split(', ') for i in output.splitlines()][::-1][1:-1][:20]
                results = [[pre_results[i][0][2:],pre_results[i][1][7:]] for i in range(len(pre_results))]

            elif keyword == 'ts':
                import re

                out1 = subprocess.check_output(['tracker','search',query_words])
                out2 = [i for i in out1.splitlines()]
                out3 = [re.sub('\x1b[^m]*m', '', i).strip() for i in out2[1:]]
                pre_results = list(chunks(out3,3))[:-1]
                print(pre_results)
                results = [[pre_results[i][1],pre_results[i][0][7:]] for i in range(len(pre_results))]

            elif keyword == 'lc':
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


            if yad_path == None:
                items = []
                for i in results:
                    items.append(ExtensionResultItem(icon='images/gnome.png',
                                                     name='%s' %i[0],
                                                     description="%s" %i[1],
                                                     on_enter=RunScriptAction("xdg-open '%s'" %i[1], None)))
            else:
                items = []
                for i in results:
                    items.append(ExtensionResultItem(icon='images/gnome.png',
                                                     name='%s' %i[0],
                                                     description="%s" %i[1],                                              
                                                     on_enter=RunScriptAction("~/.cache/ulauncher_cache/extensions/com.github.dalanicolai.gnome-tracker-extension/ulaction '%s'" %i[1].replace("%20"," "), None)))       


        return RenderResultListAction(items)

if __name__ == '__main__':
    GnomeTrackerExtension().run()
