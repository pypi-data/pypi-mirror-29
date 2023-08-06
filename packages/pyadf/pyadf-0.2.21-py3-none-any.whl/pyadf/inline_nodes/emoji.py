from .inline_node import InlineNode

class Emoji(InlineNode):
    type = 'emoji'
    def __init__(self, shortname, emoji_id=None, fallback=None):
        self.shortname = shortname
        self.id = emoji_id
        self.fallback = fallback

    def to_doc(self):
        attrs = {
            'shortName': ":{}:".format(self.shortname)
        }
        if (self.id != None):
            attrs['id'] = self.id
        if (self.fallback != None):
            attrs['fallback'] = self.fallback

        return {
            'type': self.type,
            'attrs': attrs
        }