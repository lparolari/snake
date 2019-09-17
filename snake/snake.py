# -*- coding: utf-8 -*-
import collections

import click
import numpy

"""Main module."""


class Game(object):
    """
    The game.
    """

    def play(self):
        # TODO: threaded environment for user input management, game management
        window = SnakeWindow()
        window.draw()


class Corner:
    """
    Corner representation for the snake.
    """
    _i = None
    _j = None

    def __init__(self, i, j):
        self._i = i
        self._j = j

    @property
    def i(self):
        return self._i

    @property
    def j(self):
        return self._j

    def __eq__(self, other):
        if not isinstance(other, Corner):
            return NotImplemented
        return self.i == other.i and self.j == other.j

    def __hash__(self):
        return hash((self.i, self.j))

    def __cmp__(self, other):
        if not isinstance(other, Corner):
            return NotImplemented
        return self.i == other.i and self.j == other.j


class Matrix:
    """
    Matrix abstraction for board's internal representation.
    """
    _matrix = None

    def __init__(self, rows, cols):
        _matrix = numpy.zeros((rows, cols))

    def set(self, i, j, v):
        self._matrix.put((i, j), v)


class Board(object):
    """
    Board management.
    """

    # TODO: implementing snake matrix with real matrix, and terminal board converting internal representation!

    _rows = None
    _cols = None
    _matrix = None

    _head_repr = 1
    _tail_repr = 2

    _snake_length = 5
    _snake_i, _snake_j = 0, 0  # snake head
    _snake_prev_direction = None
    _snake_corners = collections.deque()  # (popleft) [(0)======(N)] (pop, append)

    def __init__(self, rows, cols):
        self._rows = rows
        self._cols = cols
        self._matrix = numpy.zeros((rows, cols))  # [[self._init_char for i in range(cols)] for j in range(rows)]

    def draw(self):
        raise NotImplementedError("This method should be implemented by subclasses")

    def print_board(self):
        print('*' * (self._cols + 2))
        for i in range(self._rows):
            print('*', end='')
            for j in range(self._cols):
                print(str(self._matrix[i][j]), end='')
            print('*')
        print('*' * (self._cols + 2))

    def move(self, direction):
        prev_direction = self._snake_prev_direction

        # are the input directions valid?
        if (prev_direction == 'up' and direction == 'down'
            or prev_direction == 'down' and direction == 'up'
            or prev_direction == 'right' and direction == 'left'
            or prev_direction == 'left' and direction == 'right'): direction = prev_direction

        # pacman mode on.
        i = (self._snake_i + self._inc('i', direction) + self._rows) % self._rows
        j = (self._snake_j + self._inc('j', direction) + self._cols) % self._cols

        # is the snake eating itself?
        if Corner(i, i) in self._snake_corners:
            click.echo("Game over")

        # set snake head and tail.
        self._snake_corners.append(Corner(self._snake_i, self._snake_j))
        if len(self._snake_corners) > self._snake_length:
            self._snake_corners.popleft()
        self._snake_i = i
        self._snake_j = j

        self._snake_prev_direction = direction

        click.echo(i)  # debug
        click.echo(j)

    def update(self):
        self._empty_matrix()
        self._set(self._snake_i, self._snake_j, self._head_repr)
        for corner in self._snake_corners:
            self._set(
                corner.i,
                corner.j,
                self._tail_repr)

    def _set(self, i, j, v):
        self._matrix[i][j] = v

    def _empty_matrix(self):
        self._matrix = numpy.zeros((self._rows, self._cols))

    @staticmethod
    def _inc(axis, direction):
        if axis == 'i':
            if direction == 'up': return -1
            if direction == 'down': return 1

        if axis == 'j':
            if direction == 'left': return -1
            if direction == 'right': return 1

        return 0


class TerminalBoard(Board):
    _head_char = '@'
    _tail_char = '#'

    def __init__(self, rows, cols):
        super().__init__(rows, cols)

    def draw(self):
        print('*' * (self._cols + 2))
        for i in range(self._rows):
            print('*', end='')
            for j in range(self._cols):
                print(self._convert(self._matrix[i][j]), end='')
            print('*')
        print('*' * (self._cols + 2))

    def _convert(self, repr):
        if repr == 1: return self._head_char
        if repr == 2: return self._tail_char
        return ' '


class SnakeWindow(object):
    """
    The window manager.
    Loads the board, draws it and waits for commands.
    """
    _speed = 0.5

    _board = TerminalBoard(10, 30)  # TODO: load the board implementation based on configuration

    # TODO: implement a bounding box for snake and wrap it into a "curses pad"

    def __init__(self):
        pass

    def draw(self):
        self._board.update()
        self._board.draw()
        while True:
            self._board.move(self._input())
            self._board.update()
            self._board.draw()

    def _input(self):
        move = click.prompt("Direction")
        if move in ['w', 'a', 's', 'd']:
            return self._wasd_to_direction(move)

    @staticmethod
    def _wasd_to_direction(wasd):
        d = {'w': "up", 'a': "left", 's': "down", 'd': "right"}
        click.echo(d[wasd])
        return d[wasd]
