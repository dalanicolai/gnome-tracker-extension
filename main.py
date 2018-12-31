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
		
        query_words = event.get_argument()
        home = os.getenv("HOME")
        
        command = ['tracker', 'sparql', '-q', "SELECT nfo:fileName(?f) nie:url(?f) \
                   WHERE { ?f nie:url ?url FILTER(fn:starts-with(?url, \'file://" + home + "/\')) \
                   . ?f fts:match '"+query_words+"' } ORDER BY nfo:fileLastAccessed(?f)"]
        
        output = subprocess32.check_output(command)          
        results = [i.split(',') for i in output.splitlines()][1:-1]
        print(results)
		
        items = []
        for i in results:
            items.append(ExtensionResultItem(icon='images/gnome.png',
                                             name='%s' % i[0],
                                             description='%s' % i[1],
                                             on_enter=RunScriptAction("xdg-open %s" % (i[1]),'')))

        return RenderResultListAction(items)

if __name__ == '__main__':
    GnomeTrackerExtension().run()
