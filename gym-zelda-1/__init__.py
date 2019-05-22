"""Registration code of Gym environments in this package."""
import gym as _gym
from gym import make
from .zelda_env import Zelda1Env


# register the environment
_gym.envs.registration.register(
    id='Zelda1-v0',
    entry_point='gym_zelda_1:Zelda1Env',
    max_episode_steps=9999999,
    reward_threshold=9999999,
    nondeterministic=True,
)


# define the outward facing API of this package
__all__ = [
    make.__name__,
    Zelda1Env.__name__,
]
