# -*- coding: utf-8 -*-

"""Console script for snake."""
import sys
import click
from game import Game


@click.command()
@click.option("--mode", default="terminal", type=click.Choice(["terminal", "curses"]), help="The board mode.")
@click.option("--rows_no", default=10, type=click.IntRange(2, 1000), help="Rows number.")
@click.option("--cols_no", default=30, type=click.IntRange(2, 1000), help="Cols number.")
@click.option("--speed", default=0, type=click.IntRange(0, 20), help="An integer representing the game speed. 0 is "
                                                                     "the initial speed.")
def main(mode, rows_no, cols_no, speed):
    """
    Welcome to snake on terminal!

    Luca Parolari  <luca.parolari23@gmail.com>

    Snake on terminal is a simple implementation of the famous arcade game, on terminal obviously.
    The game is available in two modalities: the basic terminal mode, with sequential prints or the curses mode that
    redraws the screen.

    The best play experience is obtained with 'curses' mode, but the 'terminal' mode is interesting for learning
    purposes.

    Drive the snake with 'w', 'a', 's', 'd'. Use 'q' to quit.
    """

    snake = Game(mode=mode,
                 speed=speed,
                 rows_no=rows_no,
                 cols_no=cols_no)
    try:
        snake.play()
    except Exception as e:
        print(e)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
