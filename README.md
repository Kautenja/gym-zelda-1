# gym-zelda-1

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://travis-ci.com/Kautenja/gym-zelda-1.svg?branch=master
[ci-server]: https://travis-ci.com/Kautenja/gym-zelda-1
[pypi-version]: https://badge.fury.io/py/gym-zelda-1.svg
[pypi-license]: https://img.shields.io/pypi/l/gym-zelda-1.svg
[pypi-status]: https://img.shields.io/pypi/status/gym-zelda-1.svg
[pypi-format]: https://img.shields.io/pypi/format/gym-zelda-1.svg
[pypi-home]: https://badge.fury.io/py/gym-zelda-1
[python-version]: https://img.shields.io/pypi/pyversions/gym-zelda-1.svg
[python-home]: https://python.org

<img
  src="https://user-images.githubusercontent.com/2184469/58208692-dae16580-7caa-11e9-82cf-2e870c681201.gif"
  width="200px" />

An [OpenAI Gym](https://github.com/openai/gym) environment for The Legend of
Zelda (i.e., Zelda 1) on The Nintendo Entertainment System (NES) based on
the [nes-py](https://github.com/Kautenja/nes-py) emulator.

## Installation

The preferred installation of `gym-zelda-1` is from `pip`:

```shell
pip install gym-zelda-1
```

## Usage

### Python

You must import `gym_zelda_1` before trying to make an environment.
This is because gym environments are registered at runtime. By default,
`gym_zelda_1` environments use the full NES action space of 256
discrete actions. To constrain this, `gym_zelda_1.actions` provides
an action list called `MOVEMENT` (20 discrete actions) for the
`nes_py.wrappers.JoypadSpace` wrapper.

```python
from nes_py.wrappers import JoypadSpace
import gym_zelda_1
from gym_zelda_1.actions import MOVEMENT

env = gym_zelda_1.make('Zelda1-v0')
env = JoypadSpace(env, MOVEMENT)

done = True
for step in range(5000):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())
    env.render()

env.close()
```

**NOTE:** `gym_zelda_1.make` is just an alias to `gym.make` for
convenience.

**NOTE:** remove calls to `render` in training code for a nontrivial
speedup.

### Command Line

`gym_zelda_1` features a command line interface for playing
environments using either the keyboard, or uniform random movement.

```shell
gym_zelda_1 -m <`human` or `random`>
```

## Step

Info about the rewards and info returned by the `step` method.

### Reward Function

TODO: The reward function is a complicated work in progress.

### `info` dictionary

The `info` dictionary returned by the `step` method contains the following
keys:

| Key                   | Type    | Description
|:----------------------|:--------|:------------------------------------------------------|
| `current_level`       | `int`   | The current level Link is in (0 for overworld)
| `x_pos`               | `int`   | Link's _x_ position in the screen (from the left)
| `y_pos`               | `int`   | Link's _y_ position in the screen (from the top)
| `direction`           | `str`   | Link's direction as one of _{"N", "S", "E", "W"}_
| `has_candled`         | `bool`  | Whether Link has candled the current room
| `pulse_1`             | `str`   | The signal playing through pulse 1
| `pulse_2`             | `str`   | The signal playing through pulse 2
| `killed_enemies`      | `int`   | The number of enemies killed
| `number_of_deaths`    | `int`   | The number of times Link has died
| `sword`               | `str`   | The kind of sword Link has
| `number_of_bombs`     | `int`   | The number of bombs in Link's inventory
| `arrows_type`         | `str`   | The kind of arrows in Link's inventory
| `has_bow`             | `bool`  | Whether Link has the bow in his inventory
| `candle_type`         | `str`   | The type of candle in Link's inventory
| `has_whistle`         | `bool`  | Whether Link has the whistle in his inventory
| `has_food`            | `bool`  | Whether Link has food in his inventory
| `potion_type`         | `str`   | The type of potion in Link's inventory
| `has_magic_rod`       | `bool`  | Whether Link has the magic rod in his inventory
| `has_raft`            | `bool`  | Whether Link has the raft in his inventory
| `has_magic_book`      | `bool`  | Whether Link has the magic book in his inventory
| `ring_type`           | `str`   | The type of ring in Link's inventory
| `has_step_ladder`     | `bool`  | Whether Link has the step ladder in his inventory
| `has_magic_key`       | `bool`  | Whether Link has the magic key in his inventory
| `has_power_bracelet`  | `bool`  | Whether Link has the power bracelet in his inventory
| `has_letter`          | `bool`  | Whether Link has the letter in his inventory
| `is_clock_possessed`  | `bool`  | Whether the clock is possessed
| `rupees`              | `int`   | The number of rupess Link has collected
| `keys`                | `int`   | The number of keys in Link's inventory
| `heart_containers`    | `int`   | The number of heart containers that Link has
| `hearts`              | `float` | The number of remaining health Link has
| `has_boomerang`       | `bool`  | Whether Link has the boomerang in his inventory
| `has_magic_boomerang` | `bool`  | Whether Link has the magic boomerang in his inventory
| `has_magic_shield`    | `bool`  | Whether Link has the magic shield in his inventory
| `max_number_of_bombs` | `int`   | The maximum number of bombs Link can carry

## Citation

Please cite `gym-zelda-1` if you use it in your research.

```tex
@misc{gym-zelda-1,
  author = {Christian Kauten},
  title = {{The Legend of Zelda} for {OpenAI Gym}},
  year = {2019},
  publisher = {GitHub},
  howpublished = {\url{https://github.com/Kautenja/gym-zelda-1}},
}
```

## References

The following references contributed to the construction of this project.

1. [The Legend of Zelda: RAM Map](https://datacrystal.romhacking.net/wiki/The_Legend_of_Zelda:RAM_map). _Data Crystal ROM Hacking_.
2. [The Legend of Zelda: Memory Addresses](http://thealmightyguru.com/Games/Hacking/Wiki/index.php/The_Legend_of_Zelda#Memory_Addresses). _NES Hacker._
