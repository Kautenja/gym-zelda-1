"""Test cases for the Zelda 1 environment."""
from unittest import TestCase
import warnings
from gymnasium.utils.env_checker import check_env
import numpy as np
from ..zelda_env import Zelda1Env


class Zelda1EnvAPITest(TestCase):
    """Tests for the Zelda 1 environment Gymnasium API."""

    expected_info_keys = {
        'current_level',
        'x_pos',
        'y_pos',
        'direction',
        'has_candled',
        'pulse_1',
        'pulse_2',
        'killed_enemies',
        'number_of_deaths',
        'sword',
        'number_of_bombs',
        'arrows_type',
        'has_bow',
        'candle_type',
        'has_whistle',
        'has_food',
        'potion_type',
        'has_magic_rod',
        'has_raft',
        'has_magic_book',
        'ring_type',
        'has_step_ladder',
        'has_magic_key',
        'has_power_bracelet',
        'has_letter',
        'is_clock_possessed',
        'rupees',
        'keys',
        'heart_containers',
        'hearts',
        'has_boomerang',
        'has_magic_boomerang',
        'has_magic_shield',
        'max_number_of_bombs',
    }

    def test_reset_and_step_follow_gymnasium_api(self):
        """reset and step return the Gymnasium tuple shapes."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            observation, info = env.reset(seed=123)
            self.assertIsInstance(observation, np.ndarray)
            self.assertEqual((240, 256, 3), observation.shape)
            self.assertEqual(np.uint8, observation.dtype)
            self.assertEqual(self.expected_info_keys, set(info))

            result = env.step(0)
            self.assertEqual(5, len(result))
            observation, reward, terminated, truncated, info = result

            self.assertIsInstance(observation, np.ndarray)
            self.assertEqual((240, 256, 3), observation.shape)
            self.assertEqual(0.0, reward)
            self.assertIs(type(terminated), bool)
            self.assertIs(type(truncated), bool)
            self.assertFalse(terminated)
            self.assertFalse(truncated)
            self.assertEqual(self.expected_info_keys, set(info))
        finally:
            env.close()

    def test_rgb_array_render_mode_returns_frame(self):
        """The rgb_array render mode returns the current NES screen."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            observation, _ = env.reset(seed=123)
            frame = env.render()
            self.assertIs(frame, observation)
        finally:
            env.close()

    def test_gymnasium_env_checker(self):
        """The direct environment satisfies Gymnasium's environment checker."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    'ignore',
                    category=UserWarning,
                    module='gymnasium.utils.env_checker',
                )
                check_env(env, skip_close_check=True)
        finally:
            if env._env is not None:
                env.close()
