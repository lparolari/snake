import time

import numpy
from asciimatics.screen import Screen

from snake.board import Board
from snake.broadcaster import broadcaster


class Engine(object):
    _speed = 0

    def __init__(self, board):
        self._board = board
        broadcaster.listen("snake_eat", self._inc_speed)

    def start(self):
        raise NotImplementedError()

    def draw(self, *args, **kwargs):
        raise NotImplementedError()

    @property
    def speed(self):
        """
        :return: The computed game update speed.
        """
        return numpy.exp(-self._speed / 10) / 2

    @speed.setter
    def speed(self, v):
        self._speed = v

    def _inc_speed(self, _args):
        self._speed += 1


class BasicEngine(Engine):

    def start(self):
        while True:
            self._board.step()
            self.draw(matrix=self._board.matrix())

            time.sleep(self.speed)

    def draw(self, *args, **kwargs):
        matrix = kwargs['matrix']

        cast = {Board.EMPTY_REPR: " ", Board.SNAKE_HEAD_REPR: "@", Board.SNAKE_TAIL_REPR: "#", Board.FOOD_REPR: "+"}

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


class AsciimaticsEngine(Engine):

    def start(self):
        Screen.wrapper(self.draw)

    def draw(self, *args, **kwargs):
        while True:
            self._board.step()
            matrix = self._board.matrix()
            screen = args[0]

            cast = {Board.EMPTY_REPR: " ", Board.SNAKE_HEAD_REPR: "@", Board.SNAKE_TAIL_REPR: "#", Board.FOOD_REPR: "+"}

            (r, c) = matrix.shape

            screen.print_at("*" * (c + 2), 0, 0)
            for i in range(r):
                line = "*"
                for j in range(c):
                    line += cast[matrix[i][j]]
                line += "*"
                screen.print_at(line, 0, i+1)
            screen.print_at("*" * (c + 2), 0, r + 1)

            screen.refresh()

            time.sleep(self.speed)
