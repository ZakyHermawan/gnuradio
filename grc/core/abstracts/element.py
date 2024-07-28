from abc import ABC, abstractmethod
import weakref
from ..utils.descriptors import lazy_property

class AbstractElement(ABC):

    ##################################################
    # Element Validation API
    ##################################################
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def add_error_message(self, msg):
        pass

    @abstractmethod
    def get_error_messages(self):
        pass

    @abstractmethod
    def iter_error_messages(self):
        pass

    @abstractmethod
    def rewrite(self):
        pass

    @property
    @abstractmethod
    def enabled(self):
        pass

    @abstractmethod
    def get_bypassed(self):
        pass

    ##############################################
    # Tree-like API
    ##############################################
    @property
    @abstractmethod
    def parent(self):
        return self._parent()

    @abstractmethod
    def get_parent_by_type(self, cls):
        pass

    @lazy_property
    @abstractmethod
    def parent_platform(self):
        pass

    @lazy_property
    @abstractmethod
    def parent_flowgraph(self):
        pass

    @lazy_property
    @abstractmethod
    def parent_block(self):
        pass

    @abstractmethod
    def reset_parents_by_type(self):
        pass

    @abstractmethod
    def children(self):
        pass

    ##############################################
    # Type testing
    ##############################################
    is_flow_graph = False
    is_block = False
    is_dummy_block = False
    is_connection = False
    is_port = False
    is_param = False
    is_variable = False
    is_import = False
    is_snippet = False

    @abstractmethod
    def get_raw(self, name):
        pass

    @abstractmethod
    def set_evaluated(self, name, value):
        pass
