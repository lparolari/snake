import click

from snake.board import Board, GameOverException
from snake.broadcaster import broadcaster
from snake.engine import AsciimaticsEngine, BasicEngine
from snake.food import Food
from snake.keyb import keyboardManager, keyboardBuffer
from snake.snaky import Snake, PacmanNormalizationStrategy, WallNormalizationStrategy


class GameOptions(object):
    MODE_BASIC = 'basic'
    MODE_ASCIIMATICS = 'asciimatics'
    WALL_PACMAN = 'pacman'
    WALL_WALL = 'wall'

    _mode = None
    _wall_mode = None
    _rows = None
    _cols = None
    _speed = None
    _foods = None
    _eat_multiplier = None
    _initial_length = None

    def __init__(self,
                 mode=MODE_BASIC,
                 wall_mode=WALL_PACMAN,
                 rows=10, cols=10,
                 speed=0,
                 foods=3,
                 eat_multiplier=1,
                 initial_length=3):
        """
        Initialize game options. If some value is semantically incorrect it will be replaced with defaults.
        """
        if mode not in [self.MODE_BASIC, self.MODE_ASCIIMATICS]:
            mode = self.MODE_BASIC
        if rows < 10:
            rows = 10
        if cols < 10:
            cols = 10
        if speed < 0:
            speed = 0
        if foods < 0:
            foods = 0
        if eat_multiplier < 0:
            eat_multiplier = 0
        if initial_length < 1:
            initial_length = 1

        self._mode = mode
        self._wall_mode = wall_mode
        self._rows = rows
        self._cols = cols
        self._speed = speed
        self._foods = foods
        self._eat_multiplier = eat_multiplier
        self._initial_length = initial_length

    @property
    def mode(self):
        return self._mode

    @property
    def wall_mode(self):
        return self._wall_mode

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def speed(self):
        return self._speed

    @property
    def foods(self):
        return self._foods

    @property
    def eat_multiplier(self):
        return self._eat_multiplier

    @property
    def initial_length(self):
        return self._initial_length


class Game(object):

    _score = 0

    def __init__(self, options):
        # normalization strategies.
        normalization_strategy = PacmanNormalizationStrategy((options.rows, options.cols))
        if options.wall_mode == GameOptions.WALL_WALL:
            normalization_strategy = WallNormalizationStrategy((options.rows, options.cols))

        # game objects
        snake = Snake(initial_length=options.initial_length, eat_multiplier=options.eat_multiplier)
        snake.set_normalization_strategy(normalization_strategy.get())
        food = Food()
        board = Board(options.rows, options.cols, options.foods, snake, food)

        # engine
        engine = BasicEngine(board=board)
        if options.mode == GameOptions.MODE_ASCIIMATICS:
            engine = AsciimaticsEngine(board=board)

        self._engine = engine
        self._engine.speed = options.speed

        # callbacks
        keyboardManager.register("w", lambda: keyboardBuffer.bufferize("w"))
        keyboardManager.register("a", lambda: keyboardBuffer.bufferize("a"))
        keyboardManager.register("s", lambda: keyboardBuffer.bufferize("s"))
        keyboardManager.register("d", lambda: keyboardBuffer.bufferize("d"))
        keyboardManager.register("q", lambda: keyboardBuffer.bufferize("q"))

        broadcaster.listen("snake_eat", self._inc_score)

    def play(self):
        try:
            self._engine.start()
        except GameOverException as _e:
            self.game_over()

    def game_over(self):
        click.echo("###########################################")
        click.echo("                GAME OVER                 ")
        click.echo("                                          ")
        click.echo(" Your score is {},".format(self._score))
        click.echo(" {}".format(self._motivational_phrase(self._score)))
        click.echo("###########################################")
        # click.echo("")
        # click.echo("  ---")
        # click.echo("  Thanks for playing SNAKE ON TERMINAL")
        # click.echo("  Luca Parolari <luca.parolari23@gmail.com>")
        # click.echo("")
        # click.echo("  If you linked this game and/or the code behind this please leave a star")
        # click.echo("  to the github repository. If you find a bug let me know through the ")
        # click.echo("  issue tab on github.")
        # click.echo("  Link: https://github.com/lparolari/snake")

    @staticmethod
    def _motivational_phrase(score):
        if score in range(0, 8):
            return "you need to practise more ;)"
        if score in range(9, 16):
            return "wow, you are learning!"
        if score in range(17, 30):
            return "good game! :D"
        if score in range(31, 50):
            return "you are a pro gamer!"
        if score in range(51, 100):
            return "are you cheating? o.O"
        if score > 100:
            return "God mode on!"

    def _inc_score(self, _args):
        self._score += 1
