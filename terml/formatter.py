from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field
from typing import Any

from .ansi_colors import Color, EscapeSequence
from .parser import Parser, TagNode, TextNode


@dataclass
class Formatter:
    _: KW_ONLY
    parser: Parser = field(default_factory=Parser)

    def make_sequence(self, node: TagNode) -> EscapeSequence:
        # TODO:
        d = {}
        color_names = set(map(str.lower, Color._member_names_))
        attr_set = set(node.attrs)
        text_styles = {"bold", "italic", "underline"}
        # red, green, blue and etc
        if node.name in color_names:
            d["color"] = node.name
        # b -> bold and etc
        elif v := {v[0]: v for v in text_styles}.get(node.name):
            d[v] = True
        # [color=<color>]
        elif node.name == "color":
            d["color"] = node.attrs.get("#value")
        # [i red] -> [i color=red]
        if v := attr_set & color_names:
            *_, d["color"] = v
        # [b underline]
        for i in attr_set & text_styles:
            d[i] = True
        # text foreground/background
        for k in ["color", "background"]:
            if v := node.attrs.get(k):
                d[k] = v
        return EscapeSequence(**d)

    def escape(self, s: str) -> str:
        """escape start tag"""
        return self.parser.escape(s)

    def format_node(
        self,
        node: TagNode,
        esq_seq: EscapeSequence | None = None,
    ) -> str:
        esq_seq = (
            self.make_sequence(node)
            if esq_seq is None
            else esq_seq | self.make_sequence(node)
        )
        rv = ""
        for child in node.children:
            if isinstance(child, TextNode):
                rv += esq_seq.apply(child)
            else:
                rv += self.format_node(child, esq_seq)
        return rv

    def format(self, s: str, *args: Any, **kwargs: Any) -> str:
        return self.format_node(self.parser.parse(s, *args, **kwargs))


_formatter = Formatter()
format = _formatter.format
escape = _formatter.escape
del _formatter
