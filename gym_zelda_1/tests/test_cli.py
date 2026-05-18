"""Test cases for the command line interface."""
import io
from unittest import TestCase
from unittest.mock import patch

import gymnasium as gym
import numpy as np

from gym_zelda_1._app import cli
from gym_zelda_1.actions import MOVEMENT


class _DummyEnv(gym.Env):
    """Minimal Gymnasium environment for CLI dispatch tests."""

    metadata = {'render_fps': 60}
    observation_space = gym.spaces.Box(
        low=0,
        high=255,
        shape=(2, 2, 3),
        dtype=np.uint8,
    )
    action_space = gym.spaces.Discrete(256)

    def __init__(self):
        """Initialize the dummy environment."""
        super().__init__()
        self.reset_seeds = []

    def reset(self, *, seed=None, options=None):
        """Record reset seeds and return a dummy observation."""
        super().reset(seed=seed)
        self.reset_seeds.append(seed)
        return np.zeros(self.observation_space.shape, dtype=np.uint8), {}

    def step(self, action):
        """Return a non-terminal dummy transition."""
        return (
            np.zeros(self.observation_space.shape, dtype=np.uint8),
            0.0,
            False,
            False,
            {},
        )

    def render(self):
        """Return a dummy frame."""
        return np.zeros(self.observation_space.shape, dtype=np.uint8)

    def get_keys_to_action(self):
        """Return a minimal keyboard mapping."""
        return {(): 0}


class CLITest(TestCase):
    """Tests for CLI parsing and playback dispatch."""

    def test_human_mode_rejects_no_render(self):
        """Human mode requires a graphical render window."""
        stderr = io.StringIO()
        with patch('sys.stderr', new=stderr):
            with self.assertRaises(SystemExit) as raised:
                cli._get_args(['--mode', 'human', '--no-render'])

        self.assertEqual(2, raised.exception.code)
        self.assertIn('human mode requires graphical rendering', stderr.getvalue())

    def test_random_mode_rejects_nonpositive_steps(self):
        """Random mode requires a positive step count."""
        stderr = io.StringIO()
        with patch('sys.stderr', new=stderr):
            with self.assertRaises(SystemExit) as raised:
                cli._get_args(['--mode', 'random', '--steps', '0'])

        self.assertEqual(2, raised.exception.code)
        self.assertIn('--steps must be positive in random mode', stderr.getvalue())

    def test_random_no_render_does_not_request_human_render_mode(self):
        """Headless random playback does not construct a render window."""
        env = _DummyEnv()
        with patch.object(cli.gym, 'make', return_value=env) as make:
            with patch.object(cli, 'play_random') as play_random:
                result = cli.main([
                    '--mode', 'random',
                    '--steps', '5',
                    '--no-render',
                    '--seed', '123',
                    '--actionspace', 'movement',
                    '--no-progress',
                ])

        self.assertEqual(0, result)
        make.assert_called_once_with('Zelda1-v0', render_mode=None)
        play_random.assert_called_once()
        played_env = play_random.call_args.args[0]
        self.assertEqual(5, play_random.call_args.args[1])
        self.assertEqual(False, play_random.call_args.kwargs['render'])
        self.assertEqual(False, play_random.call_args.kwargs['progress'])
        self.assertEqual(len(MOVEMENT), played_env.action_space.n)

        played_env.reset()
        played_env.reset()

        self.assertEqual([123, None], env.reset_seeds)

    def test_random_render_requests_human_render_mode(self):
        """Rendered random playback follows nes_py.play render semantics."""
        env = _DummyEnv()
        with patch.object(cli.gym, 'make', return_value=env) as make:
            with patch.object(cli, 'play_random'):
                cli.main(['--mode', 'random', '--steps', '1'])

        make.assert_called_once_with('Zelda1-v0', render_mode='human')

    def test_human_mode_uses_seeded_env_without_render_mode(self):
        """Human mode delegates to play_human without Gymnasium render mode."""
        env = _DummyEnv()
        with patch.object(cli.gym, 'make', return_value=env) as make:
            with patch.object(cli, 'play_human') as play_human:
                result = cli.main(['--mode', 'human', '--seed', '7'])

        self.assertEqual(0, result)
        make.assert_called_once_with('Zelda1-v0', render_mode=None)
        play_human.assert_called_once()

        played_env = play_human.call_args.args[0]
        played_env.reset()
        played_env.reset()

        self.assertEqual([7, None], env.reset_seeds)

    def test_movement_actionspace_uses_public_preset(self):
        """The movement CLI action space maps to gym_zelda_1.actions.MOVEMENT."""
        env = cli._apply_action_space(_DummyEnv(), 'movement')

        self.assertEqual(len(MOVEMENT), env.action_space.n)
        self.assertEqual(
            [' '.join(action) for action in MOVEMENT],
            env.get_action_meanings(),
        )
