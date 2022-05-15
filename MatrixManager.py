import atexit
import time
import curses
import logging
from MatrixColumn import MatrixColumn
import MatrixUtils

SPEED_COLUMNS_WINDOWS_WIDTH = 10
SPEED_MAX_MULTIPLIER = 30
TICK_IN_SECONDS = .01


class MatrixManager:
    def __init__(self):
        logging.basicConfig(filename='git2/MatrixRain/log.txt', level=logging.DEBUG)
        self._max_x = 0
        self._max_y = 0
        self._columns = []
        self._screen = None
        self._columnSpeedWindow = []
        self.init_curses()
        atexit.register(self.end_curses, self)
        logging.debug('MatrixManager initialized')

    def init_curses(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self._screen.attron(curses.color_pair(1))
        #curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        #curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._max_x = curses.COLS - 1
        self._max_y = curses.LINES - 1
        logging.debug('... curses initialized')

    @staticmethod
    def end_curses(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def _generate_valid_column_speed(self):
        while True:
            speed = MatrixUtils.get_rand_in_range(1, SPEED_MAX_MULTIPLIER)
            speed_is_valid = True
            for i in self._columnSpeedWindow:
                if i == speed:
                    speed_is_valid = False
                    break
            if speed_is_valid:
                self._columnSpeedWindow.append(speed)
                if len(self._columnSpeedWindow) > SPEED_COLUMNS_WINDOWS_WIDTH:
                    self._columnSpeedWindow.pop(0)
                break
        return speed

    def generate_columns(self):
        self._columns = []
        for i in range(0, self._max_x):
            speed = self._generate_valid_column_speed()
            self._columns.append(MatrixColumn(i, self._max_y, speed))

    def _fill_screen(self):
        for x in range(self._max_x):
            for y in range(self._max_y):
                self._screen.addstr(y, x, '#')
                self._screen.refresh()

#        for col in self._columns:
#            col_number = col._number
#            if (col_number % 2) == 0:
#                continue
#            for symbol in col._symbols:
#                self._screen.addstr(symbol._number, col_number, str(symbol._symbol), curses.color_pair(2))
#        self._screen.refresh()

#        text_y = self._max_y // 2
#        self._screen.addstr(text_y, 10, 'M', curses.color_pair(2) | curses.A_BOLD)
#        self._screen.addstr(text_y, 20, 'A', curses.color_pair(2))
#        self._screen.addstr(text_y, 30, 'T', curses.color_pair(3))
#        self._screen.addstr(text_y, 40, 'R', curses.color_pair(2))
#        self._screen.addstr(text_y, 50, 'I', curses.color_pair(2) | curses.A_BOLD)
#        self._screen.addstr(text_y, 60, 'X', curses.color_pair(3) | curses.A_BOLD)
#        self._screen.refresh()

    def refresh_screen(self):
        for col in self._columns:
            col_number = col._number
            for symbol in col._symbols:
                self._screen.addstr(symbol._number, col_number, str(symbol._symbol), symbol._color)
        self._screen.refresh()

    def tick(self):
        for column in self._columns:
            column.tick()
        self.refresh_screen()

    def run(self):
        self.generate_columns()
        self._fill_screen()
        while True:
            time.sleep(TICK_IN_SECONDS)
            self.tick()


if __name__ == '__main__':
    manager = MatrixManager()
    manager.run()
