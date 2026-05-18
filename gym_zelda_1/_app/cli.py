"""Zelda 1 for Gymnasium."""
import argparse
import sys
import gymnasium as gym
from nes_py.play import play_human
from nes_py.play import play_random
from nes_py.wrappers import JoypadSpace
from gym_zelda_1.actions import MOVEMENT


_ACTION_SPACES = {
    'full': None,
    'movement': MOVEMENT,
}


class _SeedFirstReset(gym.Wrapper):
    """Apply a configured seed to only the first reset call."""

    def __init__(self, env, seed):
        """Initialize the wrapper with the seed to apply."""
        super().__init__(env)
        self._seed = seed
        self._pending = seed is not None

    def reset(self, *, seed=None, options=None):
        """Reset the environment, using the configured seed once."""
        if self._pending and seed is None:
            seed = self._seed
        self._pending = False
        return self.env.reset(seed=seed, options=options)

    def get_keys_to_action(self):
        """Return the keyboard mapping for the wrapped environment."""
        if hasattr(self.env, 'get_keys_to_action'):
            return self.env.get_keys_to_action()
        return self.env.unwrapped.get_keys_to_action()


def _parser():
    """Build the command line argument parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env', '-e',
        type=str,
        default='Zelda1-v0',
        choices=['Zelda1-v0'],
        help='The environment to play'
    )
    parser.add_argument('--mode', '-m',
        type=str,
        default='human',
        choices=['human', 'random'],
        help='The execution mode for the environment.'
    )
    parser.add_argument('--render',
        action=argparse.BooleanOptionalAction,
        default=True,
        help='Render frames to a graphical window.'
    )
    parser.add_argument('--steps', '-s',
        type=int,
        default=500,
        help='The number of random steps to take.',
    )
    parser.add_argument('--seed',
        type=int,
        default=None,
        help='Seed for the first environment reset.',
    )
    parser.add_argument('--actionspace', '--action-space',
        type=str,
        default='full',
        choices=sorted(_ACTION_SPACES.keys()),
        help='The action space preset to use.',
    )
    parser.add_argument('--no-progress',
        action='store_false',
        dest='progress',
        help='Disable the random-mode progress bar.',
    )
    parser.set_defaults(progress=True)
    return parser


def _get_args(argv=None):
    """Parse command line arguments and return them."""
    parser = _parser()
    args = parser.parse_args(argv)
    if args.mode == 'human' and not args.render:
        parser.error('human mode requires graphical rendering')
    if args.mode == 'random' and args.steps <= 0:
        parser.error('--steps must be positive in random mode')
    return args


def _apply_action_space(env, actionspace):
    """Apply a CLI-selected action space to an environment."""
    actions = _ACTION_SPACES[actionspace]
    if actions is None:
        return env
    return JoypadSpace(env, actions)


def _apply_first_reset_seed(env, seed):
    """Apply a seed to the first reset when one was provided."""
    if seed is None:
        return env
    return _SeedFirstReset(env, seed)


def _make_env(args):
    """Build and wrap the environment requested by CLI arguments."""
    render_mode = 'human' if args.mode == 'random' and args.render else None
    env = gym.make(args.env, render_mode=render_mode)
    env = _apply_action_space(env, args.actionspace)
    return _apply_first_reset_seed(env, args.seed)


def main(argv=None):
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args(argv)
    # build the environment with the given ID
    env = _make_env(args)
    # play the environment with the given mode
    if args.mode == 'human':
        play_human(env)
    else:
        play_random(
            env,
            args.steps,
            render=args.render,
            progress=args.progress,
        )
    return 0


if __name__ == '__main__':
    sys.exit(main())


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
