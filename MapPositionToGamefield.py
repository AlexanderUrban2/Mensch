# Author: Christoph Böhringer, Alexander Urban
# Date: 05/28/2020
# Version: 1.3

# 0: (0, 4) is the starting field of the green player
"""
    desc:
        - get gamefield coordinates by converting a pawn's current position into coordinates
          the playing fields are basically a circle except for each player's yard and their finishing squares
    param:
        - position: int -> position of a pawn object on the game field
    return:
        - x: int -> x_coordinate
        - y: int -> y_coordinate
"""

map_current_position_to_coordinates = {
    0: (0, 4),
    1: (1, 4),
    2: (2, 4),
    3: (3, 4),
    4: (4, 4),
    5: (4, 3),
    6: (4, 2),
    7: (4, 1),
    8: (4, 0),
    9: (5, 0),
    10: (6, 0),
    11: (6, 1),
    12: (6, 2),
    13: (6, 3),
    14: (6, 4),
    15: (7, 4),
    16: (8, 4),
    17: (9, 4),
    18: (10, 4),
    19: (10, 5),
    20: (10, 6),
    21: (9, 6),
    22: (8, 6),
    23: (7, 6),
    24: (6, 6),
    25: (6, 7),
    26: (6, 8),
    27: (6, 9),
    28: (6, 10),
    29: (5, 10),
    30: (4, 10),
    31: (4, 9),
    32: (4, 8),
    33: (4, 7),
    34: (4, 6),
    35: (3, 6),
    36: (2, 6),
    37: (1, 6),
    38: (0, 6),
    39: (0, 5),
    110: (0, 0),
    120: (0, 1),
    130: (1, 0),
    140: (1, 1),
    210: (9, 0),
    220: (10, 0),
    230: (9, 1),
    240: (10, 1),
    310: (9, 9),
    320: (10, 9),
    330: (9, 10),
    340: (10, 10),
    410: (0, 9),
    420: (1, 9),
    430: (0, 10),
    440: (1, 10),
    1010: (1, 5),
    1020: (2, 5),
    1030: (3, 5),
    1040: (4, 5),
    2010: (5, 1),
    2020: (5, 2),
    2030: (5, 3),
    2040: (5, 4),
    3010: (9, 5),
    3020: (8, 5),
    3030: (7, 5),
    3040: (6, 5),
    4010: (5, 9),
    4020: (5, 8),
    4030: (5, 7),
    4040: (5, 6),
}
