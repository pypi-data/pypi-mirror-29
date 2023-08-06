#! /usr/bin/python3
# -*- coding: utf-8 -*-

from pyadf.group_node_children_mixin import GroupNodeChildrenMixin

class Document(GroupNodeChildrenMixin):
    type = 'doc'
    def __init__(self):
        self.content = []
        pass

    def to_doc(self):
        return {
            'body': {
                'version': 1,
                'type': self.type,
                'content': [
                    x.to_doc() for x in self.content
                ]
            }
        }
