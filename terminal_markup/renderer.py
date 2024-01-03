from __future__ import annotations

from dataclasses import KW_ONLY, dataclass, field

from .escape_sequence import Color, EscapeSequence
from .markup import MarkupParser, TagNode, TextNode

_COLOR_NAMES = set(map(str.lower, Color._member_names_))


@dataclass
class MarkupRenderer:
    """Render Markup to Terminal"""

    _: KW_ONLY
    tag_rules: dict = field(
        default_factory=lambda: {
            "b": {"bold": True},
            "bold": {"bold": True},
            "dim": {"dim": True},
            "i": {"italic": True},
            "em": {"italic": True},
            "u": {"underline": True},
            "blink": {"blink": True},
            "rev": {"reversed": True},
            "color": lambda node: {"color": node.attrs["value"]},
            # red, green and etc
            "*": lambda node: {"color": node.name}
            if node.name in _COLOR_NAMES
            else {},
        }
    )
    parser: MarkupParser = field(default_factory=MarkupParser)

    def _make_escape_sequence(self, node: TagNode) -> EscapeSequence:
        rv = self.tag_rules.get(node.name, self.tag_rules.get("*"))
        if callable(rv):
            rv = rv(node)
        rv = EscapeSequence(**rv)
        # apply attributes
        attr_set = set(node.attrs)
        style_attributes = {
            "bold",
            "dim",
            "italic",
            "underline",
            "blink",
            "reversed",
        }
        for x in attr_set & style_attributes:
            setattr(
                rv,
                x,
                node.attrs[x].strip().lower()
                not in ["false", "off", "no", "0"],
            )
        color_attributes = {"color", "background"}
        for x in attr_set & color_attributes:
            setattr(rv, x, node.attrs[x])
        if v := (attr_set & _COLOR_NAMES) - (
            style_attributes | color_attributes
        ):
            *_, rv.color = v
        return rv

    def render_node(
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
                rv += self.render_node(child, esq_seq)
        return rv

    def render(self, s: str) -> str:
        return self.render_node(self.parser.parse(s))


_renderer = MarkupRenderer()
render = _renderer.render
# del _renderer
