import atexit
import curses
import MatrixColumn
import MatrixUtils

SPEED_COLUMNS_WINDOWS_WIDTH = 10
SPEED_MAX_MULTIPLIER = 30


class MatrixManager:
    def __init__(self):
        self._max_x = 0
        self._max_y = 0
        self._columns = []
        self._screen = None
        self._columnSpeedWindow = []
        self.init_curses()
        atexit.register(self.end_curses())

    def init_curses(self):
        self._screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)

        curses.start_color()
        #curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        #curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self._max_x = curses.COLS - 1
        self._max_y = curses.LINES - 1

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
            self._columns[i] = MatrixColumn(i, self._max_y, speed)