from enum import Enum
from position import Position

# Colors
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (220, 220, 220)

# Information about tetrominoes
TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']

SHAPES = {
    'I': [[CYAN, CYAN, CYAN, CYAN]],    # 1 1 1 1

    'O': [[YELLOW, YELLOW],             # 1 1
          [YELLOW, YELLOW]],            # 1 1

    'T': [[BLACK, PURPLE, BLACK],       # 0 1 0
          [PURPLE, PURPLE, PURPLE]],    # 1 1 1

    'S': [[BLACK, GREEN, GREEN],        # 0 1 1
          [GREEN, GREEN, BLACK]],       # 1 1 0

    'Z': [[RED, RED, BLACK],            # 1 1 0
          [BLACK, RED, RED]],           # 0 1 1

    'J': [[BLUE, BLACK, BLACK],         # 1 0 0
          [BLUE, BLUE, BLUE]],          # 1 1 1

    'L': [[BLACK, BLACK, ORANGE],       # 0 1 1
          [ORANGE, ORANGE ,ORANGE]]     # 1 1 1
}

SHAPE_COLORS = {
    'I': CYAN,
    'O': YELLOW,
    'T': PURPLE,
    'S': GREEN,
    'Z': RED,
    'J': BLUE,
    'L': ORANGE
}

INITIAL_PIVOTS = {
    'I': Position(1, 0),
    'O': Position(0, 0),
    'T': Position(1, 1),
    'S': Position(1, 1),
    'Z': Position(1, 0),
    'J': Position(1, 1),
    'L': Position(1, 1)
}

# Information about grid.
GRID_HEIGHT = 20
GRID_WIDTH = 10
GRID_CELL_SIZE = 30

# Information about buttons.
BUTTON_HEIGHT = 100
BUTTON_WIDTH = 300

#Information about screen.
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1200

# Various Engine constants
class FontAlignment(Enum):
	LEFT = 0
	CENTER = 1
	RIGHT = 2
	TOP = 3
	MIDDLE = 4
	BOTTOM = 5

MB_LEFT = 1
MB_RIGHT = 3
