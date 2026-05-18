"""Test cases for the Zelda 1 environment."""
from unittest import TestCase
import warnings
from gymnasium.utils.env_checker import check_env
import numpy as np
from ..zelda_env import CONTINUE_SCREEN_PULSE_2
from ..zelda_env import DEATH_SPIRAL_PULSE_2
from ..zelda_env import REWARD_POLICY
from ..zelda_env import TERMINATION_POLICY
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

    def test_reward_and_termination_contract_is_explicit(self):
        """Zelda1-v0 is a zero-reward non-terminal sandbox."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            env.reset(seed=123)

            self.assertEqual(
                'navigation_state_inspection_sandbox_zero_reward',
                REWARD_POLICY,
            )
            self.assertEqual(
                'death_recovery_non_terminal_sandbox',
                TERMINATION_POLICY,
            )
            self.assertEqual(0.0, env._get_reward())
            self.assertIs(type(env._get_terminated()), bool)
            self.assertFalse(env._get_terminated())
        finally:
            env.close()

    def test_health_and_death_cues_are_characterized(self):
        """Health and death/continue cue RAM bytes match the v0 contract."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            env.reset(seed=123)

            env.ram[0x066F] = 0x20
            env.ram[0x0670] = 255
            self.assertEqual(1.0, env._hearts_remaining)
            self.assertIs(type(env._is_low_health), bool)
            self.assertTrue(env._is_low_health)
            self.assertFalse(env._needs_death_recovery)

            env.ram[0x0670] = 0
            self.assertEqual(0.0, env._hearts_remaining)
            self.assertFalse(env._is_low_health)
            self.assertTrue(env._needs_death_recovery)
            self.assertFalse(env._get_terminated())

            env.ram[0x0607] = DEATH_SPIRAL_PULSE_2
            self.assertTrue(env._is_death_spiral)
            self.assertFalse(env._is_continue_screen)
            self.assertEqual('Death Spiral', env._pulse_2_IM_type)

            env.ram[0x0607] = CONTINUE_SCREEN_PULSE_2
            self.assertFalse(env._is_death_spiral)
            self.assertTrue(env._is_continue_screen)
            self.assertEqual('Continue Screen', env._pulse_2_IM_type)
        finally:
            env.close()

    def test_death_recovery_advances_until_hearts_return(self):
        """Zero-health recovery presses start until Link has health again."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            env.reset(seed=123)
            env.ram[0x066F] = 0x20
            env.ram[0x0670] = 0
            actions = []

            def frame_advance(action):
                actions.append(action)
                if len(actions) == 2:
                    env.ram[0x0670] = 255

            env._frame_advance = frame_advance
            env._recover_from_zero_health()

            self.assertEqual([8, 0], actions)
            self.assertEqual(1.0, env._hearts_remaining)
        finally:
            env.close()

    def test_did_step_does_not_recover_after_terminal_step(self):
        """Post-step recovery is skipped when a terminal flag is already set."""
        env = Zelda1Env(render_mode='rgb_array')
        try:
            env.reset(seed=123)
            calls = []

            env._recover_from_zero_health = lambda: calls.append('recover')
            env._wait_for_scroll = lambda: calls.append('scroll')
            env._skip_boring_actions = lambda: calls.append('boring')
            env._skip_inventory_scroll = lambda: calls.append('inventory')

            env._did_step(done=True)
            self.assertEqual([], calls)

            env._did_step(done=False)
            self.assertEqual(['recover', 'scroll', 'boring', 'inventory'], calls)
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
