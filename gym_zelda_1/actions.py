"""A list of discrete actions that are legal in the game."""


# actions for movement
MOVEMENT = [
    ['NOOP'],
    ['start'], # to enter and exit inventory
    ['A'],
    ['B'],
    # right combinations
    ['right'],
    ['right', 'A'],
    ['right', 'B'],
    ['right', 'A', 'B'],
    # left combinations
    ['left'],
    ['left', 'A'],
    ['left', 'B'],
    ['left', 'A', 'B'],
    # up combinations
    ['up'],
    ['up', 'A'],
    ['up', 'B'],
    ['up', 'A', 'B'],
    # down combinations
    ['down'],
    ['down', 'A'],
    ['down', 'B'],
    ['down', 'A', 'B'],
]
