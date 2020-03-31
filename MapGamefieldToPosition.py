# Startposition ist Startfeld von Grün

map_position = {
    0: "0 4",
    1: "1 4",
    2: "2 4",
    3: "3 4",
    4: "4 4",
    5: "4 3",
    6: "4 2",
    7: "4 1",
    8: "4 0",
    9: "5 0",
    10: "6 0",
    11: "6 1",
    12: "6 2",
    13: "6 3",
    14: "6 4",
    15: "7 4",
    16: "8 4",
    17: "9 4",
    18: "10 4",
    19: "10 5",
    20: "10 6",
    21: "9 6",
    22: "8 6",
    23: "7 6",
    24: "6 6",
    25: "6 7",
    26: "6 8",
    27: "6 9",
    28: "6 10",
    29: "5 10",
    30: "4 10",
    31: "4 9",
    32: "4 8",
    33: "4 7",
    34: "4 6",
    35: "3 6",
    36: "2 6",
    37: "1 6",
    38: "0 6",
    39: "0 5",
    110: "0 0",
    120: "0 1",
    130: "1 0",
    140: "1 1",
    210: "0 9",
    220: "0 10",
    230: "1 9",
    240: "1 10",
    310: "0 9",
    320: "1 9",
    330: "0 10",
    340: "1 10",
    410: "9 9",
    420: "9 10",
    430: "10 9",
    440: "10 10",
}


def get_coordinates(position: int) -> (int, int):
    x, y = map_position[position].split()
    print(x, y)
    return x, y
