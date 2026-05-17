"""Zelda 1 for Gymnasium."""
import argparse
import gymnasium as gym
from nes_py.play import play_human
from nes_py.play import play_random


def _get_args():
    """Parse command line arguments and return them."""
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
    parser.add_argument('--steps', '-s',
        type=int,
        default=500,
        help='The number of random steps to take.',
    )
    return parser.parse_args()


def main():
    """The main entry point for the command line interface."""
    # parse arguments from the command line (argparse validates arguments)
    args = _get_args()
    # build the environment with the given ID
    render_mode = 'human' if args.mode == 'random' else None
    env = gym.make(args.env, render_mode=render_mode)
    # play the environment with the given mode
    if args.mode == 'human':
        play_human(env)
    else:
        play_random(env, args.steps)


if __name__ == '__main__':
    main()


# explicitly define the outward facing API of this module
__all__ = [main.__name__]
