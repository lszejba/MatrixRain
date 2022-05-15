from MatrixSymbol import MatrixSymbol
import MatrixUtils
import logging


class MatrixColumn:
    def __init__(self, column_number, column_size, speed=1):
        # How many ticks between action in this column
        self._speed = speed
        # Current's group head index (might be negative if group isn't on screen yet
        self._group_head = -MatrixUtils.get_pause_size()
        # Number of ticks to another action
        self._ticks_left = -self._group_head * self._speed
        # Number of symbols in current group
        self._symbols_left = MatrixUtils.get_group_size()
        # Column index
        self._number = column_number
        # Number of symbols in column
        self._max_size = column_size
        self._symbols = []
        for i in range(self._max_size):
            self._symbols.append(MatrixSymbol(i))
#        logging.debug('create for %s', str(self))

    def __str__(self):
        return "MatrixColumn - speed: {0}, group_head: {1}, ticks_left: {2}, symbols_left: {3}, number: {4}, max_size: {5}".format(self._speed, self._group_head, self._ticks_left, self._symbols_left, self._number, self._max_size)

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    def tick(self):
        logging.debug('tick() for %s', str(self))
        self._ticks_left = self._ticks_left - 1
        logging.debug('  ...ticks_left %d', self._ticks_left)
        if self._ticks_left > 0:
            return
        # Process tick
        self._ticks_left = self._speed
        logging.debug('  ...ticks_left %d', self._ticks_left)
        # Move group head down
        self._group_head = self._group_head + 1
        logging.debug('  ...group_head %d', self._group_head)
        if self._group_head >= 0:
            if self._group_head == self._max_size:  # bottom of the screen
                self._group_head = self._group_head - 1
                self._symbols_left = self._symbols_left - 1
                if self._symbols_left == 0:  # current group is all gone, prepare new one
                    self._group_head = -MatrixUtils.get_pause_size()
                    self._symbols_left = MatrixUtils.get_group_size()
                    return
                # TODO: How to allow more than one group in given column
                # TODO: (Currently we wait till whole group is gone before creating new one)
            else:  # head of group is not at the bottom yet, activate next symbol
                logging.debug('  ...trying to set_ticks_left...')
                self._symbols[self._group_head].set_ticks_left(self._symbols_left)
            for symbol in self._symbols:
                symbol.tick()
