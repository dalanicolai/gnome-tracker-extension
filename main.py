import subprocess32
import os

from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction


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

        
        if keyword == 'gt':
            print('wat is dit', event.get_keyword())
            command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) . ?f fts:match '"+query_words+"' } ORDER BY nfo:fileLastAccessed(?f)"]
            
            output = subprocess32.check_output(command)          
            results = [i.split(', ') for i in output.splitlines()][::-1][1:-1][:20]
            print(results[0][1])
            import sys
            print(sys.version)

            items = []
            for i in results:
                items.append(ExtensionResultItem(icon='images/gnome.png',
                                                 name='%s' %i[0][2:],
                                                 description="%s" %i[1][7:],
                                                 on_enter=RunScriptAction("~/.cache/ulauncher_cache/extensions/com.github.dalanicolai.gnome-tracker-extension/ulaction '%s'" %i[1][7:].replace("%20"," "), None)))        


        elif keyword == 'df':
            print('wat is dit', event.get_keyword())
            from search import search
            output = search(query_words,28834)
#            for i in results:                                
 #               print(i.getFilename() + "\t" + i.getPathStr())
            results = [[doc.getFilename(),doc.getPathStr()] for doc in output]
            print("dit is", output[0].getPathStr())

            items = []
            for i in results:
                items.append(ExtensionResultItem(icon='images/docfetcher.png',
                                                 name='%s' %i[0],
                                                 description="%s" %i[1],
                                                 on_enter=RunScriptAction("~/.cache/ulauncher_cache/extensions/com.github.dalanicolai.gnome-tracker-extension/ulaction '%s'" %i[1].replace("%20"," "), None)))      
        
		
        



        return RenderResultListAction(items)

if __name__ == '__main__':
    GnomeTrackerExtension().run()
