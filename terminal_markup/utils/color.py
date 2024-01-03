from __future__ import annotations

import string
from typing import NamedTuple


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
