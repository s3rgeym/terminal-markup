from argparse import ArgumentParser, FileType

from .renderer import render


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        help="input file",
        default="-",
        type=FileType(),
    )
    args = parser.parse_args()
    print(render(args.input.read()))
