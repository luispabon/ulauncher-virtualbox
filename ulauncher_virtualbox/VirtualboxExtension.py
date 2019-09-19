from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.event import KeywordQueryEvent
from .KeywordQueryEventListener import KeywordQueryEventListener


class VirtualboxExtension(Extension):
    def __init__(self):
        super(VirtualboxExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
