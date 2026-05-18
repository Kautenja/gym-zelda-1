"""Test cases for the Gymnasium registered environments."""
from unittest import TestCase
import gymnasium as gym
import numpy as np
import gym_zelda_1
from .. import Zelda1Env, make
from .._registration import make as registration_make


class Zelda1RegistrationTest(TestCase):
    """Tests for the public Zelda 1 environment registration."""

    def test_public_api_is_stable(self):
        """The package exports only the stable public Gymnasium helpers."""
        self.assertEqual(['make', 'Zelda1Env'], gym_zelda_1.__all__)
        self.assertIs(gym_zelda_1.Zelda1Env, Zelda1Env)

    def test_make_aliases_gymnasium_make(self):
        """The package make helper remains a Gymnasium make alias."""
        self.assertIs(make, gym.make)
        self.assertIs(gym_zelda_1.make, gym.make)
        self.assertIs(registration_make, gym.make)

    def test_registration_policy_is_explicit(self):
        """Zelda1-v0 uses Gymnasium's checker and no TimeLimit wrapper."""
        spec = gym.spec('Zelda1-v0')

        self.assertEqual('Zelda1-v0', spec.id)
        self.assertEqual('gym_zelda_1:Zelda1Env', spec.entry_point)
        self.assertTrue(spec.nondeterministic)
        self.assertFalse(spec.disable_env_checker)
        self.assertIsNone(spec.max_episode_steps)

    def test_make_registered_env_with_rgb_array_render_mode(self):
        """Zelda1-v0 can be made and stepped with the Gymnasium API."""
        env = gym.make('Zelda1-v0', render_mode='rgb_array')
        try:
            observation, info = env.reset(seed=123)
            self.assertIsInstance(observation, np.ndarray)
            self.assertIsInstance(info, dict)
            self.assertIn('current_level', info)

            result = env.step(0)
            self.assertEqual(5, len(result))
            observation, reward, terminated, truncated, info = result

            self.assertIsInstance(observation, np.ndarray)
            self.assertIsInstance(reward, float)
            self.assertIs(type(terminated), bool)
            self.assertIs(type(truncated), bool)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertIn('x_pos', info)
            self.assertIn('y_pos', info)
            self.assertIsNotNone(env.render())
        finally:
            env.close()
