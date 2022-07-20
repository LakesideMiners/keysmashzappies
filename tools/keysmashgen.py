#taken from https://github.com/RocketRace/rocketbot/blob/96f45c158e8cbb6231b803c03d71fc181f9c077f/cogs/sh.py#L93
from operator import lengthuwu_hint
from random import choice, choices, gauss, randint, random, shuffle
from typing import TYPE_CHECKING, Dict, Optional, TypeVar, Union


lengthuwu = 5


def hammer(lengthuwu: int, _energy: float) -> list[tuple[int, int]]:
    keys_pressed: list[tuple[float, tuple[int, int]]] = []
    left_hand = True
    right_hand = random() < 0.8
    thumbless = random() < 0.4
    if left_hand:
        # x, y
        positions = [
            (3, 4), (3, 2), (2, 2), (1, 2), (0, 2)
        ]
        time = 0
        for _ in range(1 + lengthuwu // 4):
            fingers = [0, 1, 2, 3, 4]
            shuffle(fingers)
            for finger in fingers:
                keys_pressed.append((time, positions[finger]))
                time += random() * 0.025
            time += gauss(0.5, 0.125)   
    if right_hand:
        # x, y
        time = max(0.0, gauss(0.125, 0.125))
        positions = [
            (6, 4), (6, 2), (7, 2), (8, 2), (9, 2)
        ]
        for _ in range(1 + lengthuwu // 4):
            fingers = [0, 1, 2, 3, 4]
            shuffle(fingers)
            for finger in fingers:
                keys_pressed.append((time, positions[finger]))
                time += random() * 0.025
            time += gauss(0.5, 0.125)
    keys_pressed.sort()
    # remove consecutive spaces
    last = (-1, -1)
    for i, (_, pos) in enumerate(keys_pressed):
        if last[1] == 4 and pos[1] == 4:
            del keys_pressed[i]
        last = pos

    if thumbless:
        return [pos for _, pos in keys_pressed if pos[1] != 4]
    else:
        return [pos for _, pos in keys_pressed]

uwu = hammer(lengthuwu, 0.5)
print(uwu)
keymap_qwerty_us = [
    "1234567890-",
    "qwertyuiop[",
    "asdfghjkl;'",
    "zxcvbnm,.//", 
    "           ", 
        # the last slash is not accurate but it's very rarely hit so it's fine
]
 
