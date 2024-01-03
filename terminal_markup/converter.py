from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field

from .escape_sequence import Color, EscapeSequence
from .markup import MarkupParser, TagNode, TextNode

_COLOR_NAMES = set(map(str.lower, Color._member_names_))


@dataclass
class MarkupConverter:
    _: KW_ONLY
    tag_rules: dict = field(
        default_factory=lambda: {
            "b": {"bold": True},
            "bold": {"bold": True},
            "dim": {"dim": True},
            "i": {"italic": True},
            "em": {"italic": True},
            "u": {"underline": True},
            "color": lambda node: {"color": node.attrs["value"]},
            # red, green and etc
            "*": lambda node: {"color": node.name}
            if node.name in _COLOR_NAMES
            else {},
        }
    )
    parser: MarkupParser = field(default_factory=MarkupParser)

    def _make_escape_sequence(self, node: TagNode) -> EscapeSequence:
        rv = self.tag_rules.get(node.name, self.tag_rules["*"])
        if callable(rv):
            rv = rv(node)
        rv = EscapeSequence(**rv)
        # apply attributes
        attr_set = set(node.attrs)
        style_attributes = {"bold", "dim", "italic", "underline"}
        for x in attr_set & style_attributes:
            setattr(
                rv, x, node.attrs[x].lower() not in ["false", "off", "no", "0"]
            )
        color_attributes = {"color", "background"}
        for x in attr_set & color_attributes:
            setattr(rv, x, node.attrs[x])
        if v := attr_set & _COLOR_NAMES - (style_attributes | color_attributes):
            *_, rv.color = v
        return rv

    def escape(self, s: str) -> str:
        """escape start tag"""
        return self.parser.escape(s)

    def convert_node(
        self,
        node: TagNode,
        esq_seq: EscapeSequence | None = None,
    ) -> str:
        assert isinstance(node, TagNode)
        esq_seq = (
            esq_seq | self._make_escape_sequence(node)
            if esq_seq
            else self._make_escape_sequence(node)
        )
        rv = ""
        for child in node.children:
            if isinstance(child, TextNode):
                rv += esq_seq.apply(child) if esq_seq else child
            else:
                rv += self.convert_node(child, esq_seq)
        return rv

    def convert(self, s: str) -> str:
        return self.convert_node(self.parser.parse(s))


_conv = MarkupConverter()
convert = _conv.convert
escape = _conv.escape
