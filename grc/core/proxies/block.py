from ..abstracts import AbstractBlock, AbstractElement
from ..blocks._flags import Flags
from ..base import Element


class BlockProxy(AbstractBlock, Element):

    def __init__(self, real_block):
        self._real_block = real_block

        self.is_block = real_block.is_block
        if self.is_block:
            self.STATE_LABELS = real_block.STATE_LABELS

            self.key = real_block.key
            self.label = real_block.label
            self.category = real_block.category
            self.vtype = real_block.vtype
            self.flags = real_block.flags
            self.documentation = real_block.documentation
            self.doc_url = real_block.doc_url
            
            self.value = real_block.value
            self.asserts = real_block.asserts

            self.templates = real_block.templates
            self.parameters_data = real_block.parameters_data
            self.inputs_data = real_block.inputs_data
            self.outputs_data = real_block.outputs_data

            self.extra_data = real_block.extra_data
            self.loaded_from = real_block.loaded_from

            self.params = real_block.params
            self.sinks = real_block.sinks
            self.sources = real_block.sources
            self.active_sources = real_block.active_sources
            self.active_sinks = real_block.active_sinks
            self.states = real_block.states
            self.flags = real_block.flags
            self.block_namespace = real_block.namespace
            self.deprecated = real_block.deprecated
            self.current_bus_structure = real_block.current_bus_structure

            self.asserts = getattr(real_block.asserts, 'asserts', [])
            self.inputs = getattr(real_block, 'inputs', [])
            self.outputs = getattr(real_block, 'outputs', [])
            self.cpp_templates = getattr(real_block, 'cpp_templates', {})
            self.orig_cpp_templates = None

            if Flags.HAS_CPP in self.flags and self.enabled and not (self.is_virtual_source() or self.is_virtual_sink()):
                # This is a workaround to allow embedded python blocks/modules to load as there is
                # currently 'cpp' in the flags by default caused by the other built-in blocks
                if hasattr(self, 'cpp_templates'):
                    # The original template, in case we have to edit it when transpiling to C++
                    self.orig_cpp_templates = self.cpp_templates

    def get_bus_structure(self, direction):
        return self._real_block.get_bus_structure(direction)

    def rewrite(self):
        self._real_block.rewrite()

    def update_bus_logic(self):
        self._real_block.update_bus_logic()

    def validate(self):
        self._real_block.validate()

    def _run_asserts(self):
        self._real_block._run_asserts()

    def _validate_generate_mode_compat(self):
        self._real_block._validate_generate_mode_compat()

    def _validate_output_language_compat(self):
        self._real_block._validate_output_language_compat()

    def _validate_var_value(self):
        self._real_block._validate_var_value()

    def __str__(self):
        return str(self._real_block)

    def __repr__(self):
        return repr(self._real_block)

    @property
    def name(self):
        return self._real_block.name

    @property
    def is_virtual_or_pad(self):
        return self._real_block.is_virtual_or_pad

    @property
    def is_variable(self):
        return self._real_block.is_variable

    @property
    def is_import(self):
        return self._real_block.is_import

    @property
    def is_snippet(self):
        return self._real_block.is_snippet

    @property
    def comment(self):
        return self._real_block.comment

    @property
    def state(self):
        return self._real_block.state

    @state.setter
    def state(self, value):
        self._real_block.state = value

    @property
    def enabled(self):
        return self._real_block.enabled

    @property
    def bus_sink(self):
        return self._real_block.bus_sink

    @bus_sink.setter
    def bus_sink(self, value):
        self._real_block.bus_sink = value

    @property
    def bus_source(self):
        return self._real_block.bus_source

    @bus_source.setter
    def bus_source(self, value):
        self._real_block.bus_source = value

    @property
    def bus_structure_source(self):
        return self._real_block.bus_structure_source

    @property
    def bus_structure_sink(self):
        return self._real_block.bus_structure_sink

    def get_var_make(self):
        return self._real_block.get_var_make()

    def get_cpp_var_make(self):
        return self._real_block.get_cpp_var_make()

    def get_var_value(self):
        return self._real_block.get_var_value()

    def get_callbacks(self):
        return self._real_block.get_callbacks()

    def get_cpp_callbacks(self):
        return self._real_block.get_cpp_callbacks()

    def format_expr(self, py_type):
        return self._real_block.format_expr(py_type)

    def get_cpp_value(self, pyval, vtype=None) -> str:
        return self._real_block.get_cpp_value(pyval, vtype)

    def is_virtual_sink(self):
        return self._real_block.is_virtual_sink()

    def is_virtual_source(self):
        return self._real_block.is_virtual_source()

    def is_deprecated(self):
        return self._real_block.is_deprecated()

    def get_bypassed(self):
        return self._real_block.get_bypassed()

    def set_bypassed(self):
        return self._real_block.set_bypassed()

    def can_bypass(self):
        return self._real_block.can_bypass()

    def ports(self):
        return self._real_block.ports()

    def active_ports(self):
        return self._real_block.active_ports()

    def children(self):
        return self._real_block.children()

    def connections(self):
        return self._real_block.connections()

    def get_sink(self, key):
        return self._real_block.get_sink(key)

    def get_source(self, key):
        return self._real_block.get_source(key)

    @property
    def namespace(self):
        return self._real_block.namespace

    @property
    def namespace_templates(self):
        return self._real_block.namespace_templates

    def evaluate(self, expr):
        return self._real_block.evaluate(expr)

    def export_data(self):
        return self._real_block.export_data()

    def import_data(self, name, states, parameters, **_):
        return self._real_block.import_data(name, states, parameters, **_)

    def filter_bus_port(self, ports):
        return self._real_block.filter_bus_port(ports)

    def type_controller_modify(self, direction):
        return self._real_block.type_controller_modify(direction)

    def form_bus_structure(self, direc):
        return self._real_block.form_bus_structure(direc)

    def bussify(self, direc):
        return self._real_block.bussify(direc)
