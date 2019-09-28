import click

from board import TerminalBoard, CursesBoard
from keyb import keyboardManager, keyboardBuffer


class Game(object):

    _board = None

    def __init__(self, mode, rows_no, cols_no, speed):
        if mode == "terminal":
            self._board = TerminalBoard(rows_no, cols_no)
        elif mode == "curses":
            self._board = CursesBoard(rows_no, cols_no)
        else:
            self._board = TerminalBoard(rows_no, cols_no)  # default
        # board created

        self._board._speed = speed  # TODO: add setter

        keyboardManager.register("w", lambda: keyboardBuffer.bufferize("w"))
        keyboardManager.register("a", lambda: keyboardBuffer.bufferize("a"))
        keyboardManager.register("s", lambda: keyboardBuffer.bufferize("s"))
        keyboardManager.register("d", lambda: keyboardBuffer.bufferize("d"))
        keyboardManager.register("q", lambda: keyboardBuffer.bufferize("q"))

    def play(self):
        self._board.start()
        self._board.game_over_callback = self.game_over

    def game_over(self):
        click.echo("Game over!")
