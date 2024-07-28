from abc import ABC, abstractmethod
from typing import List, Set, Optional, Iterator, Iterable, Tuple, Union, OrderedDict
from .element import AbstractElement

class AbstractFlowGraph(ABC):

    @abstractmethod
    def __init__(self, parent: 'Element'):
        pass

    @abstractmethod
    def imports(self) -> List[str]:
        pass

    @abstractmethod
    def get_variables(self) -> List['Element']:
        pass

    @abstractmethod
    def get_parameters(self) -> List['Element']:
        pass

    @abstractmethod
    def get_snippets_dict(self, section=None) -> List[dict]:
        pass

    @abstractmethod
    def _get_snippets(self) -> List['Element']:
        """
        Get a set of all code snippets (Python) in this flow graph namespace.

        Returns:
            a list of code snippets
        """
        pass

    @abstractmethod
    def get_monitors(self) -> List['Element']:
        pass

    @abstractmethod
    def get_python_modules(self) -> Iterator[Tuple[str, str]]:
        pass

    @abstractmethod
    def iter_enabled_blocks(self) -> Iterator['Element']:
        pass

    @abstractmethod
    def get_enabled_blocks(self) -> List['Element']:
        pass

    @abstractmethod
    def get_bypassed_blocks(self) -> List['Element']:
        pass

    @abstractmethod
    def get_enabled_connections(self) -> List['Element']:
        pass

    @abstractmethod
    def get_option(self, key) -> 'Param.EvaluationType':
        pass

    @abstractmethod
    def get_run_command(self, file_path, split=False) -> Union[str, List[str]]:
        pass

    @abstractmethod
    def get_imported_names(self) -> Set[str]:
        pass

    @abstractmethod
    def get_block(self, name) -> 'Block':
        pass

    @abstractmethod
    def get_elements(self) -> List['Element']:
        pass

    @abstractmethod
    def children(self) -> Iterable['Element']:
        pass

    @abstractmethod
    def rewrite(self):
        pass

    @abstractmethod
    def evaluate(self, expr: str, namespace: Optional[dict] = None, local_namespace: Optional[dict] = None):
        pass

    @abstractmethod
    def new_block(self, block_id, **kwargs) -> 'Block':
        pass

    @abstractmethod
    def connect(self, porta, portb, params=None):
        pass

    @abstractmethod
    def disconnect(self, *ports) -> None:
        pass

    @abstractmethod
    def remove_element(self, element) -> None:
        pass

    @abstractmethod
    def export_data(self) -> OrderedDict[str, str]:
        pass

    @abstractmethod
    def import_data(self, data) -> bool:
        pass

    @abstractmethod
    def _reload_imports(self, namespace: dict) -> dict:
        """
        Load imports; be tolerant about import errors.
        """
        pass

    @abstractmethod
    def _reload_modules(self, namespace: dict) -> dict:
        pass

    @abstractmethod
    def _reload_parameters(self, namespace: dict) -> dict:
        """
        Load parameters. Be tolerant of evaluation failures.
        """
        pass

    @abstractmethod
    def _reload_variables(self, namespace: dict) -> dict:
        """
        Load variables. Be tolerant of evaluation failures.
        """
        pass

    @abstractmethod
    def _renew_namespace(self) -> None:
        """
        Renew the namespace to get rid of invalid entries.
        """
        pass
