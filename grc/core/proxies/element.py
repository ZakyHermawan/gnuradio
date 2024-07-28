from ..abstracts import AbstractElement
import weakref


class ElementProxy(AbstractElement):

    def __init__(self, element):
        self._element = element
        self._parent = element._parent
        self._error_messages = element._error_messages

    def validate(self):
        self._element.validate()

    def is_valid(self):
        return self._element.is_valid()

    def add_error_message(self, msg):
        self._element.add_error_message(msg)

    def get_error_messages(self):
        return self._element.get_error_messages()

    def iter_error_messages(self):
        return self._element.iter_error_messages()

    def rewrite(self):
        self._element.rewrite()

    @property
    def enabled(self):
        return self._element.enabled

    def get_bypassed(self):
        return self._element.get_bypassed()

    def get_parent_by_type(self, cls):
        return self._element.get_parent_by_type(cls)

    @property
    def parent_platform(self):
        return self._element.parent_platform

    @property
    def parent_flowgraph(self):
        return self._element.parent_flowgraph

    @property
    def parent_block(self):
        return self._element.parent_block

    def reset_parents_by_type(self):
        self._element.reset_parents_by_type()

    def children(self):
        return self._element.children()

    def get_raw(self, name):
        return self._element.get_raw(name)

    def set_evaluated(self, name, value):
        self._element.set_evaluated(name, value)
