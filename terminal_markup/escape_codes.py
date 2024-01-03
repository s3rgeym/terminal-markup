from __future__ import annotations

import string
from dataclasses import KW_ONLY, MISSING, Field, dataclass, fields
from enum import Enum
from typing import ClassVar, Iterable, NamedTuple

from .utils.color import RGB
from .utils.enum import CaseInsensetiveEnum

# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# print('\x1b[38:5:1mtest\x1b[0m')


class EscapeCode(CaseInsensetiveEnum):
    def __str__(self) -> str:
        return str(self.value)


# TODO: можно использовать 256 цветов
Color = EscapeCode(
    "olor",
    ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"],
    start=0,
)

assert Color("Red") == Color(Color.RED) == Color.RED

TextStyle = EscapeCode(
    "TextStyle",
    ["BOLD", "DIM", "ITALIC", "UNDERLINE", "BLINK"],
    start=1,
)


@dataclass
class EscapeSequence:
    _: KW_ONLY
    bold: bool = False
    dim: bool = False
    italic: bool = False
    underline: bool = False
    color: str | RGB | None = None
    background: str | RGB | None = None
    CSI: ClassVar[str] = "\x1b["

    def gen_sequence(self) -> Iterable[int]:
        for x in ["bold", "dim", "italic", "underline"]:
            if getattr(self, x):
                yield TextStyle(x).value
        for color, color_offset in [
            (self.color, 30),
            (self.background, 40),
        ]:
            if color is None:
                continue
            if isinstance(color, str):
                color = RGB.from_hex(color) or color
            if isinstance(color, RGB):
                yield color_offset + 8  # включаем расширенный цветовой режим
                yield 2  # указываем что используется 24-bit
                yield from color
                continue
            try:
                yield Color(color).value + color_offset
            except ValueError:
                pass

    def apply(self, s: str) -> str:
        if seq := ";".join(map(str, self.gen_sequence())):
            return f"{self.CSI}{seq}m{s}{self.CSI}m"
        return s

    def extend(self, other: EscapeSequence) -> EscapeSequence:
        # TODO: переписать
        d = self.__dict__.copy()
        # Берем поля other, чьи значения отличны от дефолтных
        field: Field
        for field in fields(self.__class__):
            # Нужно ли?
            if field.name not in other.__dict__:
                continue
            if field.default is not MISSING:
                default_value = field.default
            else:
                default_value = field.default_factory()
            if other.__dict__[field.name] != default_value:
                d[field.name] = other.__dict__[field.name]
        return EscapeSequence(**d)

    # a | b
    __or__ = extend
