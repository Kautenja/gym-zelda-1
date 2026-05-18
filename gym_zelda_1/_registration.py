"""Gymnasium environment registration for gym_zelda_1."""
import gymnasium as _gym


make = _gym.make


_gym.envs.registration.register(
    id='Zelda1-v0',
    entry_point='gym_zelda_1:Zelda1Env',
    nondeterministic=True,
)


__all__ = [
    'make',
]
