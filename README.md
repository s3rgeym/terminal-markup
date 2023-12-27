# terml

Terminal Markup Language based on BBCode.

Inspired by [Go:tml](https://github.com/liamg/tml) and [Python:rich](https://github.com/Textualize/rich).

Installation:

```bash
pip install terml
poetry add terml
```

## Examples

```python
from terml import format

print(format("[b][color=#f70000 background=yellow] WARNING [/color]:[/b] [magenta]Life leads to [i blue underline]Death[/i].[/magenta]"))
```

## Tags

| Tag | Description |
| --- | --- |
| `b` | Bold text |
| `i` | Italic text |
| `u` | Underline text |
| `[color=<color>]`, `<color name>` | Set foreground color |

Non-existent tags do not cause errors.

## Common attributes

| Attribute | Description |
| -- | -- |
| `bold`, `italic`, `underline` | Apply the same style |
| `<color name>`, `color=<color>` | Set foreground color |
| `background=<color>` | Set background color |

Unknown attributes are ignored.

## Colors

Color name: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`. Also supported HEX-codes like `#deadbeef`.
