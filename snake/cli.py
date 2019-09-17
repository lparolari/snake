# -*- coding: utf-8 -*-

"""Console script for snake."""
import sys
import click

from snake import Game


@click.command()
def main(args=None):
    """Console script for snake."""
    click.echo("Replace this message by putting your code into "
               "snake.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")

    click.echo("Welcome to snake on terminal!")
    click.echo("Starting...")

    snake = Game()
    snake.play()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
