# Changelog

All notable changes to `gym-zelda-1` are documented in this file.

This changelog is reconstructed from local Git tags, release-oriented commit
history, `README.md`, and current package metadata in `pyproject.toml`.

## [0.3.0] - Unreleased

### Changed

- Migrated the environment package from the legacy Gym API to Gymnasium, including
  the modern `reset` and `step` call conventions used in the README examples.
- Raised the supported runtime to Python 3.13+ and aligned dependency floors with
  `gymnasium>=1.0.0` and `nes-py>=9.0.0`.
- Replaced legacy `setup.py`-driven packaging with `pyproject.toml`.
- Replaced Travis CI and makefile-centric release automation with GitHub Actions,
  a repo-local `main.sh` workflow, and trusted PyPI publishing guidance.
- Clarified wrapper bootstrap usage so callers import `gym_zelda_1` before
  creating environments.

### Notes for 1.0.0

- A natural major-version follow-up is to lock down the long-term public API after
  the Gymnasium migration, especially around reward semantics, termination
  semantics, and compatibility guarantees.

## [0.2.2] - 2019-06-02

### Fixed

- Tightened package metadata and module exports in a small follow-up patch release.

## [0.2.1] - 2019-06-02

### Changed

- Refreshed README usage guidance and simplified CLI packaging details.

## [0.2.0] - 2019-05-22

### Added

- Added the `MOVEMENT` action list for use with `nes_py.wrappers.JoypadSpace`.
- Added environment registration coverage to help protect the public import path.

### Changed

- Removed default frame and reward limits from the environment wrapper behavior.
- Expanded README usage instructions for Python and command-line workflows.

## [0.1.1] - 2019-05-22

### Fixed

- Shipped a quick stability patch across the environment implementation and
  packaging metadata after the initial release.

## [0.1.0] - 2019-05-22

### Added

- Initial public release of the Zelda NES wrapper with the `Zelda1-v0`
  environment registration.
- Early support for skipping intro, text, start-screen, inventory, and scrolling
  transitions to make rollouts less fragile.
- Initial Zelda-specific state exposure, including level, position, direction,
  audio pulse, health, inventory, and map-related getters surfaced through the
  environment `info` dictionary.
