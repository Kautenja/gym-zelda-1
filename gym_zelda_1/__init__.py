"""Public Gymnasium environments exposed by this package."""
from .zelda_env import Zelda1Env
from ._registration import make


# define the outward facing API of this package
__all__ = [
    'make',
    'Zelda1Env',
]
