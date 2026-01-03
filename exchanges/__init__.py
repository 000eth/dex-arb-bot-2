from .nado import NadoExchange
from .ethereal import EtherealExchange
from .pacifica import PacificaExchange
from .extended import ExtendedExchange
from .variational import VariationalExchange

EXCHANGES = [
    NadoExchange(),
    EtherealExchange(),
    PacificaExchange(),
    ExtendedExchange(),
    VariationalExchange(),
]
