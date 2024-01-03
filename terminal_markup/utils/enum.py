from __future__ import annotations

from enum import Enum


class CaseInsensetiveEnum(Enum):
    @classmethod
    def _missing_(cls, value: object):
        for member in cls:
            if member.name.lower() == value.lower():
                return member
