"""Test cases for the gym registered environments."""
from unittest import TestCase
from .. import make


class ShouldMakeEnv:
    """A test case for making an arbitrary environment."""
    # the environments ID
    env_id = None
    # the random seed to apply
    seed = None

    def _test_env(self, env_id):
        env = make(env_id)
        if self.seed is not None:
            env.seed(self.seed)
        env.reset()
        _state, _reward, _done, info = env.step(0)
        self.assertIn('current_level', info)
        env.close()

    def test(self):
        if isinstance(self.env_id, str):
            self._test_env(self.env_id)
        elif isinstance(self.env_id, list):
            for env_id in self.env_id:
                self._test_env(env_id)


class ShouldMakeZelda1(ShouldMakeEnv, TestCase):
    # the environment ID for The Legend of Zelda
    env_id = 'Zelda1-v0'
