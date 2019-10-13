import sys
import click
from snake.game import Game, GameOptions


@click.command()
@click.option("--engine",
              default=GameOptions.MODE_ASCIIMATICS,
              type=click.Choice([GameOptions.MODE_BASIC, GameOptions.MODE_ASCIIMATICS]),
              help="The game engine: determine how the game looks and behave. "
                   "Choose `{}` for the best game experience, `{}` for better portability."
                   .format(GameOptions.MODE_ASCIIMATICS, GameOptions.MODE_BASIC))
@click.option("--wall-mode",
              default="pacman",
              type=click.Choice([GameOptions.WALL_PACMAN, GameOptions.WALL_WALL]),
              help="The walls mode. If `{}` mode is chose the snake will pass through walls, otherwise if "
                   "`{}` is chosen the snake will die hitting the wall."
                   .format(GameOptions.WALL_PACMAN, GameOptions.WALL_WALL))
@click.option("--rows-no",
              default=10,
              type=click.IntRange(2, 1000),
              help="The board width. (Please note that in terminal vertical chars size is larger than the horizontal "
                   "one, this may seem to make the snake go faster. Try to keep `rows-no` half of `cols-no`).")
@click.option("--cols-no",
              default=30,
              type=click.IntRange(2, 1000),
              help="The board height. (Please note that in terminal vertical chars size is larger than the horizontal "
                   "one, this may seem to make the snake go faster. Try to keep `cols-no` twice bigger than `rows-no`).")
@click.option("--speed",
              default=0,
              type=click.INT,
              help="The snake initial speed. An integer from 0 to N, where 0 is the minimum speed and N the maximum ("
                   "technically there is no speed limit)")
@click.option("--initial-length",
              default=3,
              type=click.INT,
              help="The snake initial length. By default the snake is 3 blocks longer.")
@click.option("--eat-multiplier",
              default=1,
              type=click.INT,
              help="An integer representing the eat multiplier. The snake enlarges by `eat-multiplier` every time "
                   "that eats. By default it enlarges by one.")
@click.option("--food-no",
              default=3,
              type=click.INT,
              help="Food number on board.")
def main(engine, wall_mode, rows_no, cols_no, speed, food_no, eat_multiplier, initial_length):
    """
    Welcome to snake on terminal!

    Luca Parolari  <luca.parolari23@gmail.com>

    Snake on terminal is a simple implementation of the famous arcade game, on terminal obviously.
    The game is available with several interchangeable engines that modify how the game looks like and behaves.
    See the `--engine` options for more information.

    Drive the snake with 'w', 'a', 's', 'd'. Use 'q' to quit.

    Enjoy!
    """

    options = GameOptions(mode=engine,
                          wall_mode=wall_mode,
                          speed=speed,
                          rows=rows_no,
                          cols=cols_no,
                          foods=food_no,
                          eat_multiplier=eat_multiplier,
                          initial_length=initial_length)

    game = Game(options)

    try:
        game.play()
    except Exception as e:
        print(e)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
