import curses
import logging
import MatrixUtils

DEFAULT_COLOR = curses.COLOR_BLACK

# List of available Matrix symbols. Make sure that first one is always considered "blank" (e.q. space)
symbols = [
    ' ', 'ｦ', 'ｱ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾂ', 'ﾃ',
    'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾊ', 'ﾋ', 'ﾎ', 'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾗ', 'ﾘ', 'ﾜ', 'T',
    'H', 'E', 'M', 'A', 'R', 'I', 'X', ':', '.', '"', '=', '*', '+', '-', '|', '_', '0', '1',
    '2', '3', '4', '5', '6', '7', '8', '9']
 
total_symbols = len(symbols)


def get_random_symbol():
    return symbols[MatrixUtils.get_rand_in_range(1, total_symbols - 1)]


class MatrixSymbol:
    def set_symbol(self, symbol=None, fg_color=None, bg_color=None):
        if symbol is None:
            self._symbol = get_random_symbol()
        else:
            self._symbol = symbol
        if fg_color is None:
            self._fg_color = DEFAULT_COLOR
        else:
            self._fg_color = fg_color
        if bg_color is None:
            self._bg_color = DEFAULT_COLOR
        else:
            self._bg_color = bg_color

    def get_symbol(self):
        return self._symbol

    def clear_symbol(self):
        self._symbol = symbols[0]

    def set_colors(self, fg_color=None, bg_color=None):
        if fg_color:
            self._fg_color = fg_color
        if bg_color:
            self._bg_color = bg_color

    def __init__(self, symbol_number, symbol=None):
        self._number = symbol_number
        self._symbol = symbols[0]
        self._ticks_left = 0
        # Color is both curses.color_pair() and additional params (A_BOLD)
        self._color = curses.color_pair(1)
        self._fg_color = DEFAULT_COLOR
        self._bg_color = DEFAULT_COLOR
        self.set_symbol(symbol)
#        logging.debug('create for %s', str(self))

    def __str__(self):
        return "MatrixSymbol - number: {0}, symbol: {1}, ticks_left: {2}, color: {3}".format(self._number, str(self._symbol), self._ticks_left, self._color)

    def set_ticks_left(self, ticks_left):
        logging.debug('...setting ticks_left to %d', ticks_left)
        self._ticks_left = ticks_left

    def _cycle_colors(self):
        if self._ticks_left > 0:
            self._color = curses.color_pair(2)
        else:
            self._color = curses.color_pair(1)

    def tick(self):
        logging.debug('  tick() for %s', str(self))
        self._ticks_left = self._ticks_left - 1
        self._cycle_colors()
