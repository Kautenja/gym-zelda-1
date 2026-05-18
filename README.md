# gym-zelda-1

[![BuildStatus][build-status]][ci-server]
[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[build-status]: https://github.com/Kautenja/gym-zelda-1/actions/workflows/ci.yml/badge.svg?branch=master
[ci-server]: https://github.com/Kautenja/gym-zelda-1/actions/workflows/ci.yml
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

A [Gymnasium](https://gymnasium.farama.org/) environment for The Legend of
Zelda (i.e., Zelda 1) on The Nintendo Entertainment System (NES) based on
the [nes-py](https://github.com/Kautenja/nes-py) emulator. This wrapper keeps a
deliberately narrow, lower-maturity scope: it exposes Zelda RAM state and NES
control semantics for experimentation, while expecting users to supply their
own legally obtained ROM and task-specific training wrappers. CI currently
tests CPython 3.13 and 3.14 on macOS, Linux, and Windows.

## Installation

The preferred installation of `gym-zelda-1` is from `pip`:

```shell
pip install gym-zelda-1
```

Python 3.13 or newer is required. The supported CI targets are CPython 3.13
and 3.14.

`gym-zelda-1` does not distribute Nintendo ROM assets. Provide your own legally
obtained Zelda ROM through the package's expected local workflow.

## Usage

### Python

You must import `gym_zelda_1` before trying to make an environment.
This is because Gymnasium environments are registered at runtime. By default,
`gym_zelda_1` environments use the full NES action space of 256
discrete actions. To constrain this, `gym_zelda_1.actions` provides
an action list called `MOVEMENT` (20 discrete actions) for the
`nes_py.wrappers.JoypadSpace` wrapper.

```python
import gymnasium as gym
from nes_py.wrappers import JoypadSpace
import gym_zelda_1
from gym_zelda_1.actions import MOVEMENT

env = gym.make('Zelda1-v0', render_mode='human')
env = JoypadSpace(env, MOVEMENT)

observation, info = env.reset(seed=123)
for step in range(5000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    done = terminated or truncated
    env.render()

    if done:
        observation, info = env.reset()

env.close()
```

**NOTE:** `gym_zelda_1.make` is just an alias to `gymnasium.make` for
convenience.

**NOTE:** remove calls to `render` in training code for a nontrivial
speedup.

### Command Line

`gym_zelda_1` features a command line interface for playing
environments using either the keyboard, or uniform random movement.

Print the command-line help with:

```shell
gym_zelda_1 -h
```

```shell
gym_zelda_1 --mode human --actionspace movement
gym_zelda_1 --mode random --steps 500 --render --actionspace movement
gym_zelda_1 --mode random --steps 5000 --no-render --seed 123 --actionspace movement --no-progress
```

Use `--actionspace full` for the default 256-action NES controller space, or
`--actionspace movement` for the `gym_zelda_1.actions.MOVEMENT` preset with
`nes_py.wrappers.JoypadSpace`. Human mode always requires rendering; headless
`--no-render` playback is available in random mode.

## Step

Info about the rewards and info returned by the `step` method.

`Zelda1-v0` is a navigation and state-inspection sandbox. It exposes Zelda RAM
state through `info`, preserves the full NES action and observation contract,
and leaves task objectives such as route completion, dungeon progress, or time
limits to caller-provided wrappers.

### Reward Function

The reward is always `0.0`. This neutral reward is deliberate: the current v0
environment does not infer long-horizon Zelda progress from partial RAM signals.
Use external wrappers when training against a specific navigation, combat, or
collection objective.

### Termination and Truncation

The environment has no internal terminal condition. `terminated` is always
`False` for `Zelda1-v0`; death is treated as a non-terminal recovery sequence.
When Link reaches zero health, the environment advances through the death and
continue flow before subsequent gameplay continues.

Low health is characterized by the health meter as being above zero and at or
below one heart. The pulse 2 audio RAM byte can identify transient death and
continue cues (`Death Spiral` and `Continue Screen`), but these cues are not
used as episode lifecycle signals in v0. The registered `Zelda1-v0` spec does
not set `max_episode_steps`, so Gymnasium does not add a registration-level
`TimeLimit`; `truncated` remains `False` unless a caller applies an external
limit wrapper.

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
| `rupees`              | `int`   | The number of rupees Link has collected
| `keys`                | `int`   | The number of keys in Link's inventory
| `heart_containers`    | `int`   | The number of heart containers that Link has
| `hearts`              | `float` | The number of remaining health Link has
| `has_boomerang`       | `bool`  | Whether Link has the boomerang in his inventory
| `has_magic_boomerang` | `bool`  | Whether Link has the magic boomerang in his inventory
| `has_magic_shield`    | `bool`  | Whether Link has the magic shield in his inventory
| `max_number_of_bombs` | `int`   | The maximum number of bombs Link can carry

## Publishing

PyPI releases are published by the `Publish to PyPI` GitHub Actions workflow
through PyPI trusted publishing, not by local `twine` credentials. Configure
the PyPI project publisher with owner `Kautenja`, repository `gym-zelda-1`,
workflow filename `publish.yml`, and environment `pypi`.

Releases should follow the current GitHub Actions flow:

1. Create and push a tag that matches `pyproject.toml`'s version, with or
   without a leading `v`.
2. Let the CI workflow build and attach release artifacts for that tag.
3. Publish a GitHub Release from that tag to trigger the trusted-publishing
   workflow.

## Citation

Please cite `gym-zelda-1` if you use it in your research.

```tex
@misc{gym-zelda-1,
  author = {Christian Kauten},
  howpublished = {GitHub},
  title = {{The Legend of Zelda} for {Gymnasium}},
  URL = {https://github.com/Kautenja/gym-zelda-1},
  year = {2019},
}
```

## References

The following references contributed to the construction of this project.

1. [The Legend of Zelda: RAM Map](https://datacrystal.romhacking.net/wiki/The_Legend_of_Zelda:RAM_map). _Data Crystal ROM Hacking_.
2. [The Legend of Zelda: Memory Addresses](http://thealmightyguru.com/Games/Hacking/Wiki/index.php/The_Legend_of_Zelda#Memory_Addresses). _NES Hacker._
