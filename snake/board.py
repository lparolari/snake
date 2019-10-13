import numpy

from snake.broadcaster import broadcaster
from snake.keyb import keyboardBuffer
from snake.util import wasd_to_direction


class Entity(object):
    """
    This class conceptually represent a single or composite entity on matrix.
    Provide a method used to inform the matrix with the new values on board.
    """
    def to_list(self):
        raise NotImplementedError()


class GameOverException(Exception):
    pass


class Board(object):

    SNAKE_HEAD_REPR = 1.0
    SNAKE_TAIL_REPR = 2.0
    EMPTY_REPR = 0.0
    FOOD_REPR = 3.0

    _rows_no = 0
    _cols_no = 0
    _food_no = 0

    _snake = None
    _food = None

    _matrix = numpy.empty(())

    def __init__(self, rows_no, cols_no, food_no, snake_entity, food_entity):
        self._rows_no = rows_no
        self._cols_no = cols_no
        self._food_no = food_no
        self._snake = snake_entity
        self._food = food_entity

        # initialization
        self._update_status()  # draw the snake on matrix
        self._food.more(food_no, self._empty_points())  # add flowers
        self._update_status()  # draw also flowers on matrix

        broadcaster.listen("snake_eat", self._snake_eat)
        broadcaster.listen("snake_moved", self._snake_moved)

    def step(self):
        self._update_input()
        self._update_status()

    def matrix(self):
        """
        Build the game matrix with internal representation.
        :return:
        """
        return self._matrix.copy()

    def _update_status(self):
        """
        Update the status matrix by side effect and returns it.
        :return: A new status matrix.
        """
        self._matrix = numpy.full((self._rows_no, self._cols_no), Board.EMPTY_REPR)

        s = self._snake.to_list()

        for i in range(len(s)):
            si, sj = s[i]
            if i == 0:
                self._matrix[si][sj] = self.SNAKE_HEAD_REPR
            else:
                self._matrix[si][sj] = self.SNAKE_TAIL_REPR

        f = self._food.to_list()

        for i in range(len(f)):
            fi, fj = f[i]
            self._matrix[fi][fj] = self.FOOD_REPR

    def _update_input(self):
        """
        Keep the game alive updating things based on inputs.
        :return:
        """
        # keyboard buffer is necessary to keep the pressed keys history between discrete steps of the games.
        key = keyboardBuffer.next()

        if key == "q":
            raise GameOverException

        direction = wasd_to_direction(key)

        self._snake.move(direction)

    def _snake_moved(self, args):
        """
        Callback for snake moves.
        :param args: A tuple containing in the first element the parameter head, i.e. the head of the snake.
        """
        head = args[0]

        if head in self._snake.to_list()[1:]:
            raise GameOverException()
        if head in self._food.to_list():
            self._snake.eat()

    def _snake_eat(self, args):
        """
        Callback for snake eat.
        :param args: A tuple containing in the first element the parameter head, i.e. the head of the snake.
        :return:
        """
        head = args[0]

        self._food.eat(head)
        self._food.one(self._empty_points())

    def _empty_points(self):
        """
        :return: A list of empty points from the board.
        """
        point = []
        for i in range(self._rows_no):
            for j in range(self._cols_no):
                if self._matrix[i][j] == self.EMPTY_REPR:
                    point.append((i, j))
        return point
