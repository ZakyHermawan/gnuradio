from abc import ABC, abstractmethod
import collections
import typing

class AbstractBlock(ABC):

    @abstractmethod
    def get_bus_structure(self, direction):
        pass

    @abstractmethod
    def rewrite(self):
        pass

    @abstractmethod
    def update_bus_logic(self):
        pass

    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def _run_asserts(self):
        pass

    @abstractmethod
    def _validate_generate_mode_compat(self):
        pass

    @abstractmethod
    def _validate_output_language_compat(self):
        pass

    @abstractmethod
    def _validate_var_value(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def is_virtual_or_pad(self):
        pass

    @property
    @abstractmethod
    def is_variable(self):
        pass

    @property
    @abstractmethod
    def is_import(self):
        pass

    @property
    @abstractmethod
    def is_snippet(self):
        pass

    @property
    @abstractmethod
    def comment(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass

    @state.setter
    @abstractmethod
    def state(self, value):
        pass

    @property
    @abstractmethod
    def enabled(self):
        pass

    @property
    @abstractmethod
    def bus_sink(self):
        pass

    @bus_sink.setter
    @abstractmethod
    def bus_sink(self, value):
        pass

    @property
    @abstractmethod
    def bus_source(self):
        pass

    @bus_source.setter
    @abstractmethod
    def bus_source(self, value):
        pass

    @property
    @abstractmethod
    def bus_structure_source(self):
        pass

    @property
    @abstractmethod
    def bus_structure_sink(self):
        pass

    @abstractmethod
    def get_var_make(self):
        pass

    @abstractmethod
    def get_cpp_var_make(self):
        pass

    @abstractmethod
    def get_var_value(self):
        pass

    @abstractmethod
    def get_callbacks(self):
        pass

    @abstractmethod
    def get_cpp_callbacks(self):
        pass

    @abstractmethod
    def format_expr(self, py_type):
        pass

    @abstractmethod
    def get_cpp_value(self, pyval, vtype=None) -> str:
        pass

    @abstractmethod
    def is_virtual_sink(self):
        pass

    @abstractmethod
    def is_virtual_source(self):
        pass

    @abstractmethod
    def is_deprecated(self):
        pass

    @abstractmethod
    def get_bypassed(self):
        pass

    @abstractmethod
    def set_bypassed(self):
        pass

    @abstractmethod
    def can_bypass(self):
        pass

    @abstractmethod
    def ports(self):
        pass

    @abstractmethod
    def active_ports(self):
        pass

    @abstractmethod
    def children(self):
        pass

    @abstractmethod
    def connections(self):
        pass

    @abstractmethod
    def get_sink(self, key):
        pass

    @abstractmethod
    def get_source(self, key):
        pass

    @property
    @abstractmethod
    def namespace(self):
        pass

    @property
    @abstractmethod
    def namespace_templates(self):
        pass

    @abstractmethod
    def evaluate(self, expr):
        pass

    @abstractmethod
    def export_data(self):
        pass

    @abstractmethod
    def import_data(self, name, states, parameters, **_):
        pass

    @abstractmethod
    def filter_bus_port(self, ports):
        pass

    @abstractmethod
    def type_controller_modify(self, direction):
        pass

    @abstractmethod
    def form_bus_structure(self, direc):
        pass

    @abstractmethod
    def bussify(self, direc):
        pass
