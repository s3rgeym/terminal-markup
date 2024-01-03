# https://en.wikipedia.org/wiki/ANSI_escape_code
from __future__ import annotations

from dataclasses import KW_ONLY, MISSING, Field, dataclass, fields
from typing import ClassVar, Iterable

from .utils.color import RGB
from .utils.constant import NotSet
from .utils.enum import CaseInsensetiveEnum

# class EscapeCode(CaseInsensetiveEnum):
#     def __str__(self) -> str:
#         return str(self.value)


# https://ss64.com/bash/syntax-colors.html
Color = CaseInsensetiveEnum(
    "Color",
    [
        "BLACK",
        "MAROON",
        "GREEN",
        "OLIVE",
        "NAVY",
        "PURPLE",
        "TEAL",
        "SILVER",
        "GREY",
        "RED",
        "LIME",
        "YELLOW",
        "BLUE",
        "FUCHSIA",
        "AQUA",
        "WHITE",
    ],
    start=0,
)

assert Color("Red") == Color(Color.RED) == Color.RED

TextStyle = CaseInsensetiveEnum(
    "TextStyle",
    [
        "RESET",
        "BOLD",
        "DIM",
        "ITALIC",
        "UNDERLINE",
        "BLINK",
        "RBLINK",
        "REVERSED",
    ],
    start=0,
)


@dataclass
class EscapeSequence:
    _: KW_ONLY
    bold: bool | NotSet = NotSet
    dim: bool | NotSet = NotSet
    italic: bool | NotSet = NotSet
    underline: bool | NotSet = NotSet
    blink: bool | NotSet = NotSet
    reversed: bool | NotSet = NotSet
    color: str | RGB | NotSet = NotSet
    background: str | RGB | NotSet = NotSet
    CSI: ClassVar[str] = "\x1b["

    def gen_sequence(self) -> Iterable[int]:
        for x in ["bold", "dim", "italic", "underline", "blink", "reversed"]:
            val = getattr(self, x)
            if val is not NotSet and val:
                yield TextStyle(x).value
        for color, start_code in [
            (self.color, 38),
            (self.background, 48),
        ]:
            if color is NotSet:
                continue
            if isinstance(color, str):
                color = RGB.from_hex(color) or color
            if isinstance(color, RGB):
                yield start_code  # включаем расширенный цветовой режим
                yield 2  # указываем что используется 24-bit
                yield from color
                continue
            try:
                yield from [start_code, 5, Color(color).value]
            except ValueError:
                pass

    def apply(self, s: str) -> str:
        if seq := ";".join(map(str, self.gen_sequence())):
            return f"{self.CSI}{seq}m{s}{self.CSI}0m"
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
            # if field.default is not MISSING:
            #     default_value = field.default
            # else:
            #     default_value = field.default_factory()
            if other.__dict__[field.name] is not NotSet:
                d[field.name] = other.__dict__[field.name]
        return EscapeSequence(**d)

    # a | b
    __or__ = extend
