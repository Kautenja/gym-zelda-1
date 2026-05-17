"""Registration code of Gymnasium environments in this package."""
import gymnasium as _gym
from gymnasium import make
from .zelda_env import Zelda1Env


# register the environment
_gym.envs.registration.register(
    id='Zelda1-v0',
    entry_point='gym_zelda_1:Zelda1Env',
    nondeterministic=True,
    disable_env_checker=True,
)


# define the outward facing API of this package
__all__ = [
    make.__name__,
    Zelda1Env.__name__,
]
