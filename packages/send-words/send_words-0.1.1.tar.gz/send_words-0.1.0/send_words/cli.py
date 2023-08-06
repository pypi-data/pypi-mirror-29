# -*- coding: utf-8 -*-

"""Console script for send_words."""
import sys
import click
from send_words.send_words import sendingWords
    


@click.command()
def main(args=None):
    """Console script for send_words."""
    click.echo("Replace this message by putting your code into "
               "send_words.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    
    sendingWords('send_words/Diccionario.txt')
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
