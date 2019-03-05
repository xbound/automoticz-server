from .users import auth_namespace
from .maintanance import maintanance_namespace
from .devices import devices_namespace

__all__ = [
    'maintanance_namespace',
    'auth_namespace',
    'devices_namespace'
]