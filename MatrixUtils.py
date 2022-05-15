import random
import curses

MAX_WAIT_START_COLUMN = 30
MIN_GROUP_SIZE_DIV = 2
MAX_GROUP_SIZE_MULT = 3
MIN_PAUSE_SIZE_DIV = 2
MAX_PAUSE_SIZE_MULT = 3


def get_rand_in_range(min_value, max_value):
    return random.randrange(min_value, max_value + 1)


def _get_min_group_size():
    return curses.LINES // MIN_GROUP_SIZE_DIV


def _get_max_group_size():
    return curses.LINES * MAX_GROUP_SIZE_MULT


def get_group_size():
    return get_rand_in_range(_get_min_group_size(), _get_max_group_size())


def _get_min_pause_size():
    return curses.LINES // MIN_PAUSE_SIZE_DIV


def _get_max_pause_size():
    return curses.LINES * MAX_PAUSE_SIZE_MULT


def get_pause_size():
    return get_rand_in_range(_get_min_pause_size(), _get_max_pause_size())
