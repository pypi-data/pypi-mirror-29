# -*- coding: utf-8 -*-

"""Console script for pretty_upper."""
import sys
import click

from .pretty_upper import pu


@click.command()
@click.argument('word', type=str)
def main(word):
    if word:
        click.echo(pu(word))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
