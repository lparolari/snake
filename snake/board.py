import curses
import random
import time

import click
import numpy
from threading import Thread

from snake import Snake
from util import wasd_to_direction
from keyb import keyboardBuffer


class Board(Thread):
    SNAKE_HEAD_REPR = 1.0
    SNAKE_TAIL_REPR = 2.0
    EMPTY_REPR = 0.0
    FLOWER_REPR = 3.0

    FLOWER_NO = 3

    _speed = 0

    _rows_no = 0
    _cols_no = 0
    _matrix = numpy.empty(())

    _snake = None
    _flowers = []

    game_over_callback = None

    def __init__(self, rows_no, cols_no):
        super().__init__()
        self._rows_no = rows_no
        self._cols_no = cols_no
        self._matrix = numpy.full((rows_no, cols_no), Board.EMPTY_REPR)
        self._generate_flower()

        self._snake = Snake()
        self._snake.set_boundary(rows_no, cols_no)
        self._snake.set_normalization_mode("pacman")
        self._snake.set_eat_callback(lambda: self.inc_speed())

    def run(self):
        """
        Run the game engine.
        """
        try:
            while True:
                self._update()
                self._draw()
                time.sleep(self.speed)
        except GameOverException as e:
            self.finalize()
            self.game_over_callback()

    def finalize(self):
        """
        Finalize the board on game over event.
        """
        pass

    @property
    def speed(self):
        return numpy.exp(-self._speed/10) / 2

    def inc_speed(self):
        self._speed = self._speed + 1

    def _update_input(self):
        key = keyboardBuffer.next()

        if key == "q":
            raise GameOverException

        direction = wasd_to_direction(key)
        self._snake.move(direction)

    def _update_matrix(self):
        snake = self._snake.to_edges_coords()

        head = snake[0]
        tail = snake[1:]

        (hi, hj) = head

        self._matrix[hi][hj] = Board.SNAKE_HEAD_REPR
        for (ti, tj) in tail:
            self._matrix[ti][tj] = Board.SNAKE_TAIL_REPR

        if head in tail:
            raise GameOverException("Game over!")

        # eat a flower
        if head in self._flowers:
            self._snake.eat()
            self._flowers.remove(head)

        # flower regeneration
        if len(self._flowers) < Board.FLOWER_NO:
            tries = 0
            while len(self._flowers) < Board.FLOWER_NO and tries < 50:
                fi, fj = self._generate_flower()
                if (fi, fj) not in snake:
                    self._flowers.append((fi, fj))
                tries += 1

        for fi, fj in self._flowers:
            self._matrix[fi][fj] = Board.FLOWER_REPR

    def _generate_flower(self):
        return int(random.random() * self._rows_no) % self._rows_no, int(random.random() * self._cols_no) % self._cols_no

    def _update(self):
        self._matrix = numpy.zeros((self._rows_no, self._cols_no))

        self._update_input()
        self._update_matrix()

    def _draw(self):
        raise NotImplemented


class TerminalBoard(Board):
    """
    Basic terminal implementation for Board.
    """

    def _draw(self):
        matrix = self._matrix
        cast = {Board.EMPTY_REPR: " ", Board.SNAKE_HEAD_REPR: "@", Board.SNAKE_TAIL_REPR: "#", Board.FLOWER_REPR: "+"}

        (r, c) = matrix.shape
        print("*" * (c + 2))
        for i in range(r):
            print("*", end='')
            for j in range(c):
                print(
                    cast[matrix[i][j]],
                    end='')
            print("*")
        print("*" * (c + 2))


class CursesBoard(Board):
    """
    Curses implementation for Board.
    """
    _curses_src = None
    _curses_window = None

    def __init__(self, rows_no, cols_no):
        super().__init__(rows_no, cols_no)
        self._curses_src = curses.initscr()
        self._curses_src.clear()
        curses.noecho()
        curses.cbreak()
        self._curses_window = curses.newwin(rows_no, cols_no)

    def finalize(self):
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def _draw(self):
        matrix = self._matrix
        cast = {Board.EMPTY_REPR: " ", Board.SNAKE_HEAD_REPR: "@", Board.SNAKE_TAIL_REPR: "#", Board.FLOWER_REPR: "+"}

        (r, c) = matrix.shape
        self._curses_src.addstr(0, 0, "*" * (c + 2))
        for i in range(r):
            self._curses_src.addstr(i + 1, 0, "*")
            for j in range(c):
                self._curses_src.addstr(i + 1, j + 1, cast[matrix[i][j]])
            self._curses_src.addstr(i + 1, c + 1, "*")
        self._curses_src.addstr(r + 1, 0, "*" * (c + 2))
        self._curses_src.refresh()


class GameOverException(Exception):
    pass
