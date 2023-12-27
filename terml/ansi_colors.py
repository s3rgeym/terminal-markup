from __future__ import annotations

import string
from dataclasses import KW_ONLY, MISSING, Field, dataclass
from enum import Enum
from typing import ClassVar, Iterable, NamedTuple


# https://en.wikipedia.org/wiki/ANSI_escape_code
# https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# print('\x1b[38:5:1mtest\x1b[0m')
class CaseInsensetiveEnum(Enum):
    @classmethod
    def _missing_(cls, value: object):
        for member in cls:
            if member.name.lower() == value.lower():
                return member


class EscapeCode(CaseInsensetiveEnum):
    def __str__(self) -> str:
        return str(self.value)


# TODO: можно использовать 256 цветов
# https://tintin.mudhalla.net/info/256color/
Color = EscapeCode(
    "olor",
    ["BLACK", "RED", "GREEN", "YELLOW", "BLUE", "MAGENTA", "CYAN", "WHITE"],
    start=0,
)

assert Color("red") == Color(Color.RED) == Color.RED

TextStyle = EscapeCode(
    "TextStyle", ["NORMAL", "BOLD", "FAINT", "ITALIC", "UNDERLINE"], start=0
)


class RGB(NamedTuple):
    r: int
    g: int
    b: int

    @classmethod
    def from_hex(cls, h: str) -> RGB | None:
        """
        >>> RGB.from_hex('#7ff000')
        RGB(r=127, g=240, b=0)
        """
        if cls.is_hex(h):
            return cls.from_int(int(h[1:], 16))

    @classmethod
    def from_int(cls, v: int) -> RGB:
        return cls((v >> 16) & 255, (v >> 8) & 255, v & 255)

    @staticmethod
    def is_hex(s: str) -> bool:
        return (
            s.startswith("#")
            and len(s) == 7
            and all(c in string.hexdigits for c in s[1:])
        )


@dataclass
class EscapeSequence:
    _: KW_ONLY
    bold: bool = False
    italic: bool = False
    underline: bool = False
    color: str | RGB | None = None
    background: str | RGB | None = None
    CSI: ClassVar[str] = "\x1b["

    def gen_sequence(self) -> Iterable[int]:
        for x in ["bold", "italic", "underline"]:
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
        d = self.__dict__.copy()
        # Берем поля other, чьи значения отличны от дефолтных
        for name, field in self.__dataclass_fields__.items():
            if name not in other.__dict__:
                continue
            if field.default is not MISSING:
                default_value = field.default
            else:
                default_value = field.default_factory()
            if other.__dict__[name] != default_value:
                d[name] = other.__dict__[name]
        return EscapeSequence(**d)

    # a | b
    __or__ = extend
