import curses
import random
import time
 
"""
 
Based on C ncurses version
 
http://rosettacode.org/wiki/Matrix_Digital_Rain#NCURSES_version
 
"""
 
"""
Time between row updates in seconds
Controls the speed of the digital rain effect.
"""
 
ROW_DELAY=.075
MIN_COLUMN_ACTIVE = 10
MAX_COLUMN_ACTIVE = 30
MIN_COLUMN_INACTIVE = -20
MAX_COLUMN_INACTIVE = 40

def get_rand_in_range(min, max):
    return random.randrange(min,max+1)
 
#try:
    # Characters to randomly appear in the rain sequence.
chars = [ ' ', 'ｦ', 'ｱ', 'ｳ', 'ｴ', 'ｵ', 'ｶ', 'ｷ', 'ｹ', 'ｺ', 'ｻ', 'ｼ', 'ｽ', 'ｾ', 'ｿ', 'ﾀ', 'ﾂ', 'ﾃ', 'ﾅ', 'ﾆ', 'ﾇ', 'ﾈ', 'ﾊ', 'ﾋ', 'ﾎ', 'ﾏ', 'ﾐ', 'ﾑ', 'ﾒ', 'ﾓ', 'ﾔ', 'ﾕ', 'ﾗ', 'ﾘ', 'ﾜ', 'T', 'H', 'E', 'M', 'A', 'R', 'I', 'X', ':', '.', '"', '=', '*', '+', '-', '|', '_', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
 
total_chars = len(chars)
 
stdscr = curses.initscr()
curses.noecho()
curses.curs_set(False)
 
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
stdscr.attron(curses.color_pair(1))
 
max_x = curses.COLS - 1
max_y = curses.LINES - 1

text_row_y = max_y // 2

# Table containing all symbols visible currently on screen
symbols_table = [[' ' for x in range(curses.LINES)] for y in range(curses.COLS)] #[' '] * curses.COLS * curses.LINES

# Number of rounds column was active (positive number) or inactive (negative number)
columns_active = [ 0 ] * curses.COLS
# Speed of falling in given column
columns_speed = [ 1 ] * curses.COLS

def reset_columns():

    for i in range(max_x + 1):
        active = (get_rand_in_range(0, 100) > 20)
        speed = get_rand_in_range(0, 3) % 3
        if active:
            columns_active[i] = 1
        else:
            columns_active[i] = -1
        columns_speed[i] = columns_speed[i] + speed

#generate_new_symbols = True
round_counter = 0

text_labels = [ "Matrix Rain v0.1"]
#                "Available on Mac and Windows"]

text_labels_count = len(text_labels)

# Sets all columns to inactive
def stop_falling():
#    generate_new_symbols = False
    for i in range(max_x + 1):
        columns_active[i] = 0;

def stop_falling_except(min_col, max_col):
    if min_col < 0:
        pass
    if min_col < max_col:
        for i in range(max_x + 1):
            if i < min_col or i > max_col:
                columns_active[i] = 0

def cols_for_string(str):
    min_col = 0
    str_len = len(str)
    max_line_len = 0
    current_line_len = 0
    newline_count = 0
    for s in str:
        current_line_len = current_line_len + 1
        if s == '\n':
            newline_count = newline_count + 1
            if current_line_len > max_line_len:
                max_line_len = current_line_len
            current_line_len = 0
    if newline_count == 0:
        max_line_len = len(str)

    if max_line_len > max_x + 1:
        return 0, 0, 0, 0
    min_col_text = (max_x + 1 - max_line_len) // 2
    max_col_text = max_line_len + min_col_text
    min_col = (max_x + 1 - max_line_len) // 3
    max_col = (max_x + 1 - min_col)
    return min_col, max_col, min_col_text, max_col_text

def show_text_on_stream(str, min_col):
    col_count = 0
    text_row_offset = 0
    for s in str:
        if s == '\n':
            text_row_offset = text_row_offset + 1
            col_count = 0
#        symbols_table[min_col + col_count][text_row_y] = s
        stdscr.addstr(text_row_y + text_row_offset, min_col + col_count, s)
        col_count = col_count + 1
    stdscr.refresh()

try:
    text_index = 0
    while(True):
        min_col = 0
        max_col = 0
        min_col_text = 0
        max_col_text = 0
        round_counter = 0
        show_text = False
        reset_columns()
        current_text = text_labels[text_index]
        while(True):
            round_counter = round_counter + 1
            for i in range(max_x):
                # move all symbols in column down according to speed
                speed = columns_speed[i]
                for j in reversed(range(max_y - speed)):
                    symbols_table[i][j + speed] = symbols_table[i][j]
                # create new symbols if column is active
#                if generate_new_symbols:
                if columns_active[i] > 0:
                    for j in range(speed):
                        symbols_table[i][j] = chars[get_rand_in_range(0, total_chars -1)]
                    columns_active[i] = columns_active[i] + 1
                else:
                    for j in range(speed):
                        symbols_table[i][j] = ' ';
                    columns_active[i] = columns_active[i] - 1

            # draw table on screen
            for i in range(max_x):
                for j in range(max_y):
                    stdscr.addstr(j, i, symbols_table[i][j])

            time.sleep(ROW_DELAY)
            stdscr.refresh()

            # switch active/deactive states of columns
            for i in range(max_x):
                if columns_active[i] > MIN_COLUMN_ACTIVE:
                    if columns_active[i] + get_rand_in_range(0, MAX_COLUMN_ACTIVE - MIN_COLUMN_ACTIVE) > MAX_COLUMN_ACTIVE:
                        columns_active[i] = -1
                elif columns_active[i] < MIN_COLUMN_INACTIVE:
                    if get_rand_in_range(0, MAX_COLUMN_INACTIVE) + columns_active[i] > 0:
                        columns_active[i] = 1

            if round_counter > 20:
                min_col, max_col, min_col_text, max_col_text = cols_for_string(current_text)
#                stop_falling_except(min_col, max_col)
                show_text = True
#                stop_falling()
            if round_counter > 40:
                stop_falling()
            if round_counter > 45:
                show_text_on_stream(current_text, min_col_text)
            if round_counter > 80:
                show_text = False
                if text_index + 1 < text_labels_count:
                    text_index = text_index + 1
                break;
 
except KeyboardInterrupt as err:
    curses.endwin()
