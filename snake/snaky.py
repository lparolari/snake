from snake.board import Entity, GameOverException
from snake.broadcaster import broadcaster


class NormalizationStrategy(object):

    def _normalize(self, coord):
        raise NotImplementedError()

    def get(self):
        return self._normalize


class PacmanNormalizationStrategy(NormalizationStrategy):

    _boundary = None

    def __init__(self, boundary):
        self._boundary = boundary

    def _normalize(self, coord):
        """
        :param coord: The (i, j) coords tuple to normalize.
        :return: A tuple (i, j) normalized with a normalization method.
        """
        rows_no, cols_no = self._boundary
        i, j = coord

        i = (i + rows_no) % rows_no
        j = (j + cols_no) % cols_no

        return i, j


class WallNormalizationStrategy(NormalizationStrategy):
    _boundary = None

    def __init__(self, boundary):
        self._boundary = boundary

    def _normalize(self, coord):
        """
        :param coord: The (i, j) coords tuple to normalize.
        :return: A tuple (i, j) normalized with a normalization method.
        """
        wi, wj = self._boundary
        i, j = coord

        if i < 0 or i > wi or j < 0 or j > wj:
            raise GameOverException()

        return i, j


class Snake(Entity):

    NORM_MODE_PACMAN = "pacman"
    NORM_MODE_WALL = "wall"

    # head, t_1, .., t_n
    _edges = []
    _coords = 0, 0

    _eat_multiplier = 1

    _normalize = None

    def __init__(self, initial_length, eat_multiplier):
        self._edges = ["right" for _i in range(initial_length)]
        self._coords = (0, initial_length)
        self._eat_multiplier = eat_multiplier

    def move(self, direction):
        """
        Move the snake by the given direction, if possible. Check the input directions.
        :param direction: The new direction of the snake.
        """
        # input validation
        if direction is None or direction not in ("up", "down", "left", "right"):
            direction = self._last_move()

        # direction validation
        if (direction == "up" and self._last_move() == "down"
                or direction == "down" and self._last_move() == "up"
                or direction == "left" and self._last_move() == "right"
                or direction == "right" and self._last_move() == "left"):
            direction = self._last_move()

        # increment head coords
        i, j = self._coords
        di, dj = self._inc(direction)
        self._coords = self._normalize((i + di, j + dj))

        # add edge
        self._edges.insert(0, direction)
        self._edges.pop(-1)

        # moved event
        broadcaster.event("snake_moved", self._coords)

    def eat(self):
        """
        Make the snake longer by one.
        """
        last = self._edges[-1]

        for i in range(self._eat_multiplier):
            self._edges.append(last)

        # eat event
        d, hi, hj = self._head()
        broadcaster.event("snake_eat", (hi, hj))

    def set_normalization_strategy(self, normalization_strategy):
        self._normalize = normalization_strategy

    def _head(self):
        """
        :return: A tuple with (direction, i, j) where i, j are the head coords
        """
        i, j = self._coords
        return self._edges[0], i, j

    def _tail(self):
        """
        :return: A list of directions.
        """
        tail = self._edges[1:]
        return tail

    def _last_move(self):
        """
        :return: The last direction.
        """
        head, i, j = self._head()
        return head

    def to_list(self):
        """
        :return: A list of edges with coordinates where the first is the snake head and the rest the snake tail.
        """
        ll = []

        head, ti, tj = self._head()
        tail = self._tail()

        # head
        ll.append((ti, tj))

        di, dj = self._dec(head)
        ti, tj = self._normalize((ti + di, tj + dj))

        # tail
        for s in tail:
            ll.append((ti, tj))

            di, dj = self._dec(s)
            ti, tj = self._normalize((ti + di, tj + dj))

        return ll

    @staticmethod
    def _inc(direction):
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

    @staticmethod
    def _dec(direction):
        """
        :param direction: The direction, one in [up, down, left, right].
        :return: The tuple (delta i, delta j) based on direction with decrement by one.
        """
        i, j = Snake._inc(direction)
        return -i, -j
