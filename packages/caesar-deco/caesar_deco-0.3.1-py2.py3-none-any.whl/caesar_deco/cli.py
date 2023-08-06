# -*- coding: utf-8 -*-

"""Console script for caesar_deco."""
import sys
import click
from caesar_deco.caesar_deco import caesar_decoder

@click.command()
@click.argument('texto', type=str)
def main(texto):
    """Console script for caesar_deco."""
    caesar_decoder(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
