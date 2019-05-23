"""An OpenAI Gym environment for The Legend of Zelda."""
import collections
import os
from nes_py import NESEnv
import numpy as np


# the directory that houses this module
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))


# the path to the Zelda 1 ROM
ROM_PATH = os.path.join(MODULE_DIR, '_roms', 'Zelda_1.nes')


# a mapping of numeric values to cardinal directions
DIRECTIONS = collections.defaultdict(lambda: None, {
    0x08: 'N',
    0x04: 'S',
    0x01: 'E',
    0x02: 'W',
})


# the set of game modes that indicate a scroll is in progress
SCROLL_GAME_MODES = {4, 6, 7}


# a mapping of numeric values to string types for pulse 1
PULSE_1_IM_TYPES = collections.defaultdict(lambda: None, {
    0x80: None, # this value is unknown
    0x40: "1 Heart Warning",
    0x20: "Set Bomb",
    0x10: "Small Heart Pickup",
    0x08: "Key Pickup",
    0x04: "Magic Cast",
    0x02: "Boomerang Stun",
    0x01: "Arrow Deflected",
})


# a mapping of numeric values to string types for pulse 2
PULSE_2_IM_TYPES = collections.defaultdict(lambda: None, {
    0x80: "Death Spiral",
    0x40: "Continue Screen",
    0x20: "Enemy Burst",
    0x10: "Whistle",
    0x08: "Bomb Pickup",
    0x04: "Secret Revealed",
    0x02: "Key Appears",
    0x01: "Rupee Pickup",
})


# a mapping of numeric values to sword types
SWORD_TYPES = collections.defaultdict(lambda: None, {
    0x00: "None",
    0x01: "Sword",
    0x02: "White Sword",
    0x03: "Magical Sword",
})


# the type of arrows in Link's inventory
ARROWS_TYPES = collections.defaultdict(lambda: None, {
    0x00: "None",
    0x01: "Arrow",
    0x02: "Silver Arrow",
})


# the type of candle in Link's inventory
CANDLE_TYPES = collections.defaultdict(lambda: None, {
    0x00: "None",
    0x01: "Blue Candle",
    0x02: "Red Candle",
})


# the type of potion in Link's inventory
POTION_TYPES = collections.defaultdict(lambda: None, {
    0x00: "None",
    0x01: "Life Potion",
    0x02: "2nd Potion",
})


# the type of ring in Link's inventory
RING_TYPES = collections.defaultdict(lambda: None, {
    0x00: "None",
    0x01: "Blue Ring",
    0x02: "Red Ring",
})


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
    def _is_screen_scrolling(self):
        """Return True if the screen is scrolling, False otherwise."""
        return self.ram[0x12] in SCROLL_GAME_MODES

    @property
    def _current_level(self):
        """Return the current level Link is in."""
        return self.ram[0x10]

    @property
    def _current_save_slot(self):
        """Return the current save slot being played on."""
        return self.ram[0x16]

    @property
    def _x_pixel(self):
        """Return the current x pixel of Link's location."""
        return self.ram[0x70]

    @property
    def _y_pixel(self):
        """Return the current y pixel of Link's location."""
        return self.ram[0x84]

    @property
    def _direction(self):
        """Return the current direction that Link is facing."""
        return DIRECTIONS[self.ram[0x98]]

    @property
    def _has_candled(self):
        """Return True if Link has used a candle in the current room"""
        return bool(self.ram[0x0513])

    @property
    def _pulse_1_IM_type(self):
        """Return the IM type of pulse 1."""
        # TODO: gives "Small Heart" when text is blitting?
        return PULSE_1_IM_TYPES[self.ram[0x0605]]

    @property
    def _pulse_2_IM_type(self):
        """Return the IM type of pulse 2."""
        # TODO: gives "Bomb" when initial sword is picked up?
        return PULSE_2_IM_TYPES[self.ram[0x0607]]

    @property
    def _killed_enemy_count(self):
        """Return thee number of enemies killed on the current screen."""
        return self.ram[0x0627]

    @property
    def _number_of_deaths(self):
        """Return the number of times Link has died (for slot 1)."""
        # 0630    Number of deaths            save slot 1
        # 0631    Number of deaths            save slot 2
        # 0632    Number of deaths            save slot 3
        return self.ram[0x0630]

    @property
    def _sword(self):
        """Return the sword Link has."""
        return SWORD_TYPES[self.ram[0x0657]]

    @property
    def _number_of_bombs(self):
        """Return the number of bombs in inventory."""
        return self.ram[0x0658]

    @property
    def _arrows_type(self):
        """Return the type of arrows Link has."""
        return ARROWS_TYPES[self.ram[0x0659]]

    @property
    def _is_bow_in_inventory(self):
        """Return True if the bow is in Link's inventory."""
        return bool(self.ram[0x065A])

    @property
    def _candle_type(self):
        """Return the status of the candle Link has."""
        return CANDLE_TYPES[self.ram[0x065B]]

    @property
    def _is_whistle_in_inventory(self):
        """Return True if the candle is in Link's inventory."""
        return bool(self.ram[0x065C])

    @property
    def _is_food_in_inventory(self):
        """Return True if food is in Link's inventory."""
        return bool(self.ram[0x065D])

    @property
    def _potion_type(self):
        """Return True if potion is in Link's inventory."""
        return POTION_TYPES[self.ram[0x065E]]

    @property
    def _is_magic_rod_in_inventory(self):
        """Return True if the magic rod is in Link's inventory."""
        return bool(self.ram[0x065F])

    @property
    def _is_raft_in_inventory(self):
        """Return True if the raft is in Link's inventory."""
        return bool(self.ram[0x0660])

    @property
    def _is_magic_book_in_inventory(self):
        """Return True if the magic book is in Link's inventory."""
        return bool(self.ram[0x0661])

    @property
    def _ring_type(self):
        """Return True if the ring is in Link's inventory."""
        return RING_TYPES[self.ram[0x0662]]

    @property
    def _is_step_ladder_in_inventory(self):
        """Return True if the ladder is in Link's inventory."""
        return bool(self.ram[0x0663])

    @property
    def _is_magical_key_in_inventory(self):
        """Return True if the magic key is in Link's inventory."""
        return bool(self.ram[0x0664])

    @property
    def _is_power_bracelet_in_inventory(self):
        """Return True if the power bracelet is in Link's inventory."""
        return bool(self.ram[0x0665])

    @property
    def _is_letter_in_inventory(self):
        """Return True if the letter is in Link's inventory."""
        return bool(self.ram[0x0666])

    @property
    def _compass(self):
        """Return the mapping of which compasses are collected."""
        # 0667    Compass in Inventory        One bit per level
        # 0669    Compass in Inventory        (Level 9)

    @property
    def _map(self):
        """Return the mapping of which maps are collected."""
        # 0668    Map in Inventory            One bit per level
        # 066A    Map in Inventory            (Level 9)

    @property
    def _is_clock_possessed(self):
        """Return True if the clock is possessed."""
        return bool(self.ram[0x066C])

    @property
    def _number_of_rupees(self):
        """Return the number of rupees Link has."""
        return self.ram[0x066D]

    @property
    def _number_of_keys(self):
        """Return the number of keys Link has."""
        return self.ram[0x066E]

    @property
    def _number_of_heart_containers(self):
        """Return the number of total heart containers."""
        return (self.ram[0x066F] >> 4) + 1

    @property
    def _full_hearts_remaining(self):
        """Return the number of remaining hearts."""
        return 0x0F & self.ram[0x066F]

    @property
    def _partial_heart_remaining(self):
        """Return the amount of the partial heart remaining (percentage)."""
        return self.ram[0x0670] / 255

    @property
    def _hearts_remaining(self):
        """Return the amount of floating point remaining hears."""
        return self._full_hearts_remaining + self._partial_heart_remaining

    @property
    def _triforce_pieces(self):
        """Return the triforce pieces collected."""
        # 0671 Triforce pieces. One bit per piece

    @property
    def _is_boomerang_in_inventory(self):
        """Return True if the boomerang is in Link's inventory."""
        return bool(self.ram[0x0674])

    @property
    def _is_magic_boomerang_in_inventory(self):
        """Return True if the magic boomerang is in Link's inventory."""
        return bool(self.ram[0x0675])

    @property
    def _is_magic_shield_in_inventory(self):
        """Return True if the magic shield is in Link's inventory."""
        return bool(self.ram[0x0676])

    @property
    def _max_number_of_bombs(self):
        """Return the max number of bombs that Link can carry."""
        return self.ram[0x067C]

    # MARK: RAM Hacks

    def _skip_start_screen(self):
        """Press and release start to skip the start screen."""
        # press and release the start button 21 times
        # - kill 21 frames to get to registration
        # - kill 10 frames to get to player 1 registration
        for _ in range(31):
            self._frame_advance(8)
            self._frame_advance(0)
        # select the letter A and kill 6 frames
        for _ in range(6):
            self._frame_advance(1)
            self._frame_advance(0)
        # move the cursor to the register button
        for _ in range(3):
            self._frame_advance(4)
            self._frame_advance(0)
        # press select to register the profile and subsequently start the game
        # by killing some frames and pressing select again
        for _ in range(9):
            self._frame_advance(8)
            self._frame_advance(0)
        # skip the opening screen animation
        while self._direction is None or bool(self.ram[0x007C]):
            self._frame_advance(0)

    def _wait_for_hearts(self):
        """Skip the death animation when Link dies."""
        while self._hearts_remaining <= 0:
            self._frame_advance(8)
            self._frame_advance(0)

    def _wait_for_scroll(self):
        """Wait for the screen to stop scrolling."""
        while self._is_screen_scrolling:
            self._frame_advance(8)
            self._frame_advance(0)

    def _skip_boring_actions(self):
        """Skip actions that the agent will find boring."""
        # displaying text
        while self.ram[0x0605] == 0x10:
            # each character takes 6 frames to draw
            for _ in range(6):
                self._frame_advance(0)
        # entering / exiting cave
        while self.ram[0x0606] == 0x08:
            self._frame_advance(0)

    def _skip_inventory_scroll(self):
        """Skip the scrolling action when showing / hiding inventory."""
        while 65 < self.ram[0xFC]:
            self._frame_advance(0)

    # MARK: nes-py API calls

    def _will_reset(self):
        """Handle and RAM hacking before a reset occurs."""
        pass

    def _did_reset(self):
        """Handle any RAM hacking after a reset occurs."""
        pass

    def _did_step(self, done):
        """
        Handle any RAM hacking after a step occurs.

        Args:
            done: whether the done flag is set to true

        Returns:
            None

        """
        self._wait_for_hearts()
        self._wait_for_scroll()
        self._skip_boring_actions()
        self._skip_inventory_scroll()

    def _get_reward(self):
        """Return the reward after a step occurs."""
        # TODO: define a default reward function
        return 0

    def _get_done(self):
        """Return True if the episode is over, False otherwise."""
        # TODO: return True when game is over
        return False

    def _get_info(self):
        """Return the info after a step occurs"""
        return dict(
            current_level=self._current_level,
            x_pos=self._x_pixel,
            y_pos=self._y_pixel,
            direction=self._direction,
            has_candled=self._has_candled,
            pulse_1=self._pulse_1_IM_type,
            pulse_2=self._pulse_2_IM_type,
            killed_enemies=self._killed_enemy_count,
            number_of_deaths=self._number_of_deaths,
            sword=self._sword,
            number_of_bombs=self._number_of_bombs,
            arrows_type=self._arrows_type,
            has_bow=self._is_bow_in_inventory,
            candle_type=self._candle_type,
            has_whistle=self._is_whistle_in_inventory,
            has_food=self._is_food_in_inventory,
            potion_type=self._potion_type,
            has_magic_rod=self._is_magic_rod_in_inventory,
            has_raft=self._is_raft_in_inventory,
            has_magic_book=self._is_magic_book_in_inventory,
            ring_type=self._ring_type,
            has_step_ladder=self._is_step_ladder_in_inventory,
            has_magic_key=self._is_magical_key_in_inventory,
            has_power_bracelet=self._is_power_bracelet_in_inventory,
            has_letter=self._is_letter_in_inventory,
            is_clock_possessed=self._is_clock_possessed,
            rupees=self._number_of_rupees,
            keys=self._number_of_keys,
            heart_containers=self._number_of_heart_containers,
            hearts=self._hearts_remaining,
            has_boomerang=self._is_boomerang_in_inventory,
            has_magic_boomerang=self._is_magic_boomerang_in_inventory,
            has_magic_shield=self._is_magic_shield_in_inventory,
            max_number_of_bombs=self._max_number_of_bombs,
        )


# explicitly define the outward facing API of this module
__all__ = [Zelda1Env.__name__]
