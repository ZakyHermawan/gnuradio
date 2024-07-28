from ..blocks import Block, register_build_in
from ..blocks._build import build_params
from ..abstracts import AbstractVirtualBlock, AbstractBlock
from ..proxies import BlockProxy
from ..blocks.block import Block

@register_build_in
class VirtualSinkProxy(AbstractVirtualBlock, Block):
    key = 'virtual_sink'
    label = 'Virtual Sink'
    category = []
    documentation = {'': ''}

    flags = Block.flags
    flags.set('cpp')

    parameters_data = build_params(
        params_raw=[
            dict(label='Stream ID', id='stream_id', dtype='stream_id')],
        have_inputs=False, have_outputs=False, flags=flags, block_id=key
    )
    inputs_data = [dict(domain='stream', dtype='', direction='sink', id="0")]

    def initialize_params(self):
        super().__init__(self.parent)
        self.params['id'].hide = 'all'

    @property
    def stream_id(self):
        return self.params['stream_id'].value

@register_build_in
class VirtualSourceProxy(AbstractVirtualBlock, Block):
    key = 'virtual_source'
    label = 'Virtual Source'
    category = []
    documentation = {'': ''}

    flags = Block.flags
    flags.set('cpp')

    parameters_data = build_params(
        params_raw=[
            dict(label='Stream ID', id='stream_id', dtype='stream_id')],
        have_inputs=False, have_outputs=False, flags=flags, block_id=key
    )
    outputs_data = [dict(domain='stream', dtype='', direction='source', id="0")]

    def initialize_params(self):
        super().__init__(self.parent)
        self.params['id'].hide = 'all'

    @property
    def stream_id(self):
        return self.params['stream_id'].value
