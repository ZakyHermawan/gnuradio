from abc import ABC, abstractmethod
import itertools

class AbstractVirtualBlock(ABC):

    @abstractmethod
    def initialize_params(self):
        """Initialize parameters specific to the block."""
        pass
    
    @property
    @abstractmethod
    def stream_id(self):
        """Get the stream ID."""
        pass
