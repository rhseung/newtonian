from abc import abstractmethod, ABC
from sortedcontainers import SortedDict

from .utils import type_check, DefaultSortedDict

class AbstractUnit(ABC):
    ...
    
    @abstractmethod
    def _repr_latex_(self):
        ...
    
class BaseUnit(AbstractUnit):
    @type_check
    def __init__(self, symbol: str, dimension: Dimension):
        self.symbol = symbol
        self.dimension = dimension

    def _repr_latex_(self):
        pass