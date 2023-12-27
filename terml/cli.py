from argparse import ArgumentParser

from .formatter import format


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("input", help="input string")
    args = parser.parse_args()
    print(format(args.input))
