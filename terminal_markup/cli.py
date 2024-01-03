from argparse import ArgumentParser

from .renderer import render


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("text", help="Text goes here")
    args = parser.parse_args()
    print(render(args.text))
