"""An OpenAI Gym environment for The Legend of Zelda."""
import os
from nes_py import NESEnv
import numpy as np


# the directory that houses this module
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


# the path to the Zelda 1 ROM
ROM_PATH = os.path.join(MODULE_DIR, '_roms', 'Zelda_1.nes')


class Zelda1Env(NESEnv):
    """An environment for playing The Legend of Zelda with OpenAI Gym."""

    # the legal range of rewards for each step
    reward_range = (-float('inf'), float('inf'))

    def __init__(self):
        """Initialize a new Zelda 1 environment."""
        super().__init__(ROM_PATH)
        # reset the emulator, skip the start screen, and create a backup state
        self.reset()
        self._skip_start_screen()
        self._backup()

    # MARK: Memory access

    @property
    def _x_position(self):
        """Return the current horizontal position."""
        return self.ram[0x70]

    @property
    def _y_position(self):
        """Return the current vertical position."""
        return self.ram[0x84]

    # MARK: RAM Hacks

    def _skip_start_screen(self):
        """Press and release start to skip the start screen."""
        # press and release the start button
        # self._frame_advance(8)
        # self._frame_advance(0)
        # # Press start until the game starts
        # while self._time == 0:
        #     # press and release the start button
        #     self._frame_advance(8)
        #     # if we're in the single stage, environment, write the stage data
        #     if self.is_single_stage_env:
        #         self._write_stage()
        #     self._frame_advance(0)
        #     # run-out the prelevel timer to skip the animation
        #     self._runout_prelevel_timer()
        # # set the last time to now
        # self._time_last = self._time
        # # after the start screen idle to skip some extra frames
        # while self._time >= self._time_last:
        #     self._time_last = self._time
        #     self._frame_advance(8)
        #     self._frame_advance(0)

    # MARK: Reward Function

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        # self._time_last = 0
        # self._x_position_last = 0

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        # self._time_last = self._time
        # self._x_position_last = self._x_position

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        # # if done flag is set a reset is incoming anyway, ignore any hacking
        # if done:
        #     return
        # # if mario is dying, then cut to the chase and kill hi,
        # if self._is_dying:
        #     self._kill_mario()
        # # skip world change scenes (must call before other skip methods)
        # if not self.is_single_stage_env:
        #     self._skip_end_of_world()
        # # skip area change (i.e. enter pipe, flag get, etc.)
        # self._skip_change_area()
        # # skip occupied states like the black screen between lives that shows
        # # how many lives the player has left
        # self._skip_occupied_states()

    def _get_reward(self):
        """Return the reward after a step occurs."""
        # return self._x_reward + self._time_penalty + self._death_penalty

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        # if self.is_single_stage_env:
        #     return self._is_dying or self._is_dead or self._flag_get
        # return self._is_game_over

    def _get_info(self):
        """Return the info after a step occurs"""
        # return dict(
        #     coins=self._coins,
        #     flag_get=self._flag_get,
        #     life=self._life,
        #     score=self._score,
        #     stage=self._stage,
        #     status=self._player_status,
        #     time=self._time,
        #     world=self._world,
        #     x_pos=self._x_position,
        #     y_pos=self._y_position,
        # )


# explicitly define the outward facing API of this module
__all__ = [Zelda1Env.__name__]
