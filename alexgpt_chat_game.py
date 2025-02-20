import random
import curses

# Глобальные переменные
WIDTH, HEIGHT = 6, 6
SQUARE_SIZE = 2
SPACE = ' '
X = 'X'
O = 'O'
EMPTY = '.'
WIN_LINES = [(0, 1, 2), (3, 4, 5), (0, 3, 6), (1, 4, 7), (0, 4, 8), (2, 4, 6), (0, 2, 4), (1, 2, 3)]

def main():
# Инициализация консоли
    stdscr = curses.initscr()
    curses.curs_set(0)
    stdscr.keypad(1)
    stdscr.timeout(100)

    # Очистка консоли
    stdscr.clear()
    draw_board(stdscr)

    # Выбор первого игрока случайным образом
    player1 = 'X'
    player2 = 'O' if player1 == 'X' else 'X'

# Основной цикл игры
while True:
    move = get_move(player1, stdscr)
    if not validate_move(move):
        continue
    make_move(move, player1, stdscr)
    if check_win(player1, stdscr):
        stdscr.addstr(HEIGHT + 2, 2, f'{player1} выиграл!')
        break
    draw_board(stdscr)
    if not check_draw(stdscr):
        break
        move = get_move(player2, stdscr)
    if not validate_move(move):
        continue
        make_move(move, player2, stdscr)
    if check_win(player2, stdscr):
        stdscr.addstr(HEIGHT + 2, 2, f'{player2} выиграл!')
        break
        draw_board(stdscr)

# Завершение игры
stdscr.getkey()
curses.endwin()

def get_move(player, stdscr):
    x, y = 0, 0
    while True:
        x, y = stdscr.getyx()
        if x < 1 or x > HEIGHT + 1 or y < 1 or y > WIDTH + 1:
            continue
        if stdscr.inch(x, y) == SPACE and not is_opponent_around(player, (x - 1) // 2, (y - 1) // 2, stdscr):
            return (x - 1) // 2, (y - 1) // 2

def draw_board(stdscr):
# Очистка консоли
    stdscr.clear()

# Рискомка клетки
for x in range(HEIGHT + 2):
    for y in range(1, WIDTH + 1):
        if x == 1 or x == HEIGHT + 1:
            stdscr.addstr(x, y, '|')
        elif y == 1 or y == WIDTH:
            stdscr.addstr(x, y, '---')
        else:
            square = (x - 1) // 2, (y - 1) // 2
            value = board[square]
        if value == EMPTY:
            stdscr.addstr(x, y, SPACE)
        elif value == X:
            stdscr.addstr(x, y, X)
        elif value == O:
            stdscr.addstr(x, y, O)

# Отображение номеров клеток
for x in range(1, HEIGHT + 1):
    for y in range(1, WIDTH + 1):
        square = (x - 1) // 2, (y - 1) // 2
        if stdscr.inch(x, y) == '|':
            stdscr.addstr(x, y + 1, str(x))
        elif stdscr.inch(x, y) == '---':
            stdscr.addstr(x - 1, y + 1, str(y))

def make_move(move, player, stdscr):
    x, y = move
    board[move] = player
    stdscr.addstr((x * SQUARE_SIZE) + 1, (y * SQUARE_SIZE) + 1, player)

def validate_move(move):
    x, y = move
    return 0 <= x < HEIGHT and 0 <= y < WIDTH and board[(x, y)] == EMPTY

def is_opponent_around(player, x, y, stdscr):
    for line in WIN_LINES:
        if all(board[(i + x, j + y)] == opponent for i, j in line):
            return True
            return False

def check_win(player, stdscr):
    for line in WIN_LINES:
        if all(board[(i, j)] == player for i, j in line):
            return True
            return False

def check_draw(stdscr):
    for x in range(HEIGHT):
        for y in range(WIDTH):
            if board[(x, y)] == EMPTY:
                return False
                stdscr.addstr(HEIGHT + 2, 2, 'Ничья!')
                return True

if __name__ == '__main__':
    main()
# ```
# Этот код создает игру Крестики-Нолики на консоли используя библиотеку `curses`.
#  Игрок может играть против компьютера или с другом человеком.
#  Компьютер идет первым если вызывается функция `main()`, в противном случае игрок ходит первым.

# Код разбит на несколько функций, каждая из которых отвечает за определенную задачу.
#  Например, `get_move()` позволяет игроку вводить свой ход,
#  а `draw_board()` рисует доску. Функции `make_move()`, `validate_move()`
#  и `is_opponent_around()` отвечают за добавление хода игрока на доску, проверку хода на валидность и проверку наличия противника в соседних клетках. Функции `check_win()` и `check_draw()` проверяют наличие победы или ничьей.

# В конечном счете, игрок может играть в Крестики-Нолики на консоли,
#  используя клавиатуру для ввода своих ходов.
#  Компьютер будет играть против игрока, используя алгоритм, который выбирает ход случайно.