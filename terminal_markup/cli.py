from argparse import ArgumentParser

from .markup_converter import convert


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("input", help="input string")
    args = parser.parse_args()
    print(convert(args.input))
