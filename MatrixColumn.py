import MatrixSymbol


class MatrixColumn:
    def __init__(self, column_number, column_size, speed=1):
        self._speed = speed
        self._number = column_number
        self._max_size = column_size
        self._symbols = []
        for i in range(self._max_size):
            self._symbols.append(MatrixSymbol())

    def get_speed(self):
        return self._speed

    def set_speed(self, speed):
        self._speed = speed

    