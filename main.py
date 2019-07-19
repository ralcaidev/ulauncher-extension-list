from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.action.SetUserQueryAction import SetUserQueryAction
from ulauncher.api.shared.event import KeywordQueryEvent, PreferencesUpdateEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
import os
import json
import logging

EXT_DIR = os.environ["HOME"] + "/.cache/ulauncher_cache/extensions/"
log = logging.getLogger(__name__)
items = []


class ExtensionList(Extension):

    def __init__(self):
        super(ExtensionList, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(PreferencesUpdateEvent, PreferencesUpdateListener)


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        if len(items) == 0:
            for ext in self.get_extensions():
                items.append(ExtensionResultItem(icon=ext.icon,
                                                 name='%s (%s)' % (ext.name, ext.def_value.rstrip().upper()),
                                                 description='%s' % ext.description,
                                                 on_enter=SetUserQueryAction(ext.def_value)
                                                 ))
        term = (event.get_argument() or "").lower()
        sorted = self.sort(term)
        return RenderResultListAction(sorted)

    def sort(self, query):
        return list(filter(lambda item: query in item.get_name().lower(), items))

    def get_extensions(self):
        extensions = []
        for dir in os.listdir(EXT_DIR):
            manifest_dir = EXT_DIR + dir + "/manifest.json"

            with open(manifest_dir) as manifest:
                data = json.load(manifest)
                for pref in data["preferences"]:
                    if pref["type"] == "keyword" and pref["id"] != "exlist":
                        extensions.append(Extension(pref["name"],
                                                    data["description"],
                                                    pref["default_value"] + " ",
                                                    EXT_DIR + dir + "/" + data["icon"])
                                          )
        return extensions


class PreferencesUpdateListener(PreferencesUpdateEvent):
    items = []


class Extension:
    name = ""
    description = ""
    def_value = ""
    icon = ""

    def __init__(self, name, description, def_value, icon):
        self.name = name
        self.description = description
        self.def_value = def_value
        self.icon = icon


if __name__ == '__main__':
    ExtensionList().run()
