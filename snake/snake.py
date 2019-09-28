# -*- coding: utf-8 -*-

"""Main module."""
import click


class Snake(object):
    _normalization_mode = "pacman"
    _boundary = None
    # head, t_1, .., t_n
    _edges = ["right", "right", "right", "right", "right"]
    _coords = 0, 0

    _eat_callback = None

    def move(self, direction):
        """
        Move the snake by the given direction, if possible. Check the input directions.
        :param direction: The new direction of the snake.
        """
        # input validation
        if direction is None or direction not in ("up", "down", "left", "right"):
            direction = self.last_move()

        # direction validation
        if (direction == "up" and self.last_move() == "down"
                or direction == "down" and self.last_move() == "up"
                or direction == "left" and self.last_move() == "right"
                or direction == "right" and self.last_move() == "left"):
            direction = self.last_move()

        # increment head coords
        i, j = self._coords
        di, dj = self._inc(direction)
        self._coords = self._normalize((i + di, j + dj))

        # add edge
        self._edges.insert(0, direction)
        self._edges.pop(-1)

    def eat(self):
        """
        Make the snake longer by one.
        """
        last = self._edges[-1]
        self._edges.append(last)

        if self._eat_callback:
            self._eat_callback()

    def head(self):
        """
        :return: A tuple with (direction, i, j) where i, j are the head coords
        """
        i, j = self._coords
        return self._edges[0], i, j

    def tail(self):
        """
        :return: A list of directions.
        """
        tail = self._edges[1:]
        return tail

    def last_move(self):
        """
        :return: The last direction.
        """
        head, i, j = self.head()
        return head

    def to_edges_coords(self):
        """
        :return: A list of edges with coordinates for this snake.
        """
        ll = []

        head, ti, tj = self.head()
        tail = self.tail()

        # head
        di, dj = self._dec(head)
        ti, tj = self._normalize((ti + di, tj + dj))

        ll.append((ti, tj))

        # tail
        for s in tail:
            di, dj = self._dec(s)
            ti, tj = self._normalize((ti + di, tj + dj))

            ll.append((ti, tj))

        return ll

    def set_boundary(self, rows_no, cols_no):
        """
        Set the snake boundary.
        :param rows_no: The rows numerb.
        :param cols_no: The columns number.
        :return:
        """
        self._boundary = (rows_no, cols_no)

    def set_normalization_mode(self, mode):
        """
        Set the normalization mode.
        :param mode: The normalization mode, one on [pacman].
        """
        self._normalization_mode = mode

    def set_eat_callback(self, callback):
        self._eat_callback = callback

    def _normalize(self, coord):
        """
        :param coord: The (i, j) coords tuple to normalize.
        :return: A tuple (i, j) normalized with a normalization method.
        """
        if self._boundary is None:
            raise Exception("You need to initialize the boundary.")

        rows_no, cols_no = self._boundary
        i, j = coord

        if self._normalization_mode == "pacman":
            i = (i + rows_no) % rows_no
            j = (j + cols_no) % cols_no

        return i, j

    def _inc(self, direction):
        """
        :param direction: The direction, one in [up, down, left, right].
        :return: The tuple (delta i, delta j) based on direction with increment by one.
        """
        di, dj = 0, 0
        if direction == "up":
            di = -1
        if direction == "down":
            di = +1
        if direction == "left":
            dj = -1
        if direction == "right":
            dj = +1
        return di, dj

    def _dec(self, direction):
        """
        :param direction: The direction, one in [up, down, left, right].
        :return: The tuple (delta i, delta j) based on direction with decrement by one.
        """
        i, j = self._inc(direction)
        return -i, -j
