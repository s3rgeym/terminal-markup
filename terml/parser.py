from __future__ import annotations

import re
from abc import ABC
from dataclasses import KW_ONLY, dataclass, field
from functools import cached_property
from typing import ClassVar


# @dataclass
# class Node(ABC):
#     parent: Node | None = field(default=None, init=False, repr=False)
# class TextNode(str, Node): pass
# TextNode('test')
# TypeError: Node.__init__() takes 1 positional argument but 2 were given
class Node(ABC):
    parent: Node | None = None


class TextNode(str, Node):
    pass


@dataclass
class TagNode(Node):
    name: str
    attrs: dict = field(default_factory=dict, init=False)
    children: dict = field(default_factory=list, init=False)

    def __getitem__(self, key):
        return self.attrs[key]

    def __setitem__(self, key, value):
        self.attrs[key] = value

    def append_child(self, child: Node) -> None:
        child.parent = self
        self.children.append(child)


class RootNode(TagNode):
    pass


@dataclass
class ParseError(Exception):
    message: str
    pos: int

    def __str__(self) -> str:
        return f"parse error at {self.pos} - {self.message}"


@dataclass
class Parser:
    """BB Code Parser
    See: <https://www.bbcode.org/reference.php>"""

    _: KW_ONLY
    start_tag: str = "["
    end_tag: str = "]"
    name_re: ClassVar[re.Pattern] = re.compile(r"[a-z](-?[a-z0-9]+)*", re.I)
    whitespace_re: ClassVar[re.Pattern] = re.compile(r"\s+")

    @cached_property
    def text_re(self) -> re.Pattern:
        return re.compile(
            "("
            + "|".join(
                [
                    re.escape("\\" + self.start_tag),
                    f"[^{re.escape(self.start_tag)}]",
                ]
            )
            + ")+"
        )

    @cached_property
    def value_re(self) -> re.Pattern:
        return re.compile(
            rf"""[^{re.escape(self.start_tag + self.end_tag)}\s'"]+|"[^"]*"|'[^']*'"""
        )

    def match(self, pat: re.Pattern) -> str | None:
        if m := pat.match(self.input, self.pos):
            self.pos = m.end()
            return m.group(0)

    def consume(self, s: str) -> bool:
        assert s
        if self.input.startswith(s, self.pos):
            self.pos += len(s)
            return True
        return False

    def error(self, message: str) -> None:
        raise ParseError(message=message, pos=self.pos)

    @property
    def eof(self) -> bool:
        return self.pos >= len(self.input)

    def parse_name(self) -> str:
        if rv := self.match(self.name_re):
            return rv.lower()
        self.error("expected name")

    def consume_whitespace(self) -> bool:
        return bool(self.match(self.whitespace_re))

    def parse_attr_value(self) -> str:
        if rv := self.match(self.value_re):
            return rv[1:-1] if rv.startswith(('"', "'")) else rv
        self.error("excpected value")

    def parse_text(self) -> str | None:
        return self.match(self.text_re)

    def expect_end_tag(self) -> None:
        if not self.consume(self.end_tag):
            self.error("expected " + self.end_tag)

    def parse_open_tag(self) -> None:
        node = TagNode(self.parse_name())
        self.cur.append_child(node)
        self.cur = node
        # [color=red]...[/color]
        if self.consume("="):
            node["#value"] = self.parse_attr_value()
        # [b red bg=blue]...[/b]
        while self.consume_whitespace():
            attr = self.parse_name()
            value = ""
            if self.consume("="):
                value = self.parse_attr_value()
            node[attr] = value
        self.expect_end_tag()

    def parse_close_tag(self) -> None:
        tag = self.parse_name()
        self.expect_end_tag()
        if self.cur.name != tag:
            self.error(f"unexpected close tag {tag!r}")
        self.cur = self.cur.parent

    def parse_children(self):
        while not self.eof:
            if t := self.parse_text():
                self.cur.append_child(TextNode(self.unescape(t)))
            if self.consume(self.start_tag):
                if self.consume("/"):
                    self.parse_close_tag()
                else:
                    self.parse_open_tag()

    def escape(self, s: str) -> str:
        return s.replace(self.start_tag, "\\" + self.start_tag)

    def unescape(self, s: str) -> str:
        return s.replace("\\" + self.start_tag, self.start_tag)

    def parse(self, s: str) -> RootNode:
        self.input = s
        self.pos = 0
        self.cur = root = RootNode("root")
        self.parse_children()
        return root
