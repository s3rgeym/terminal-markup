# terml

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/terml)]() [![PyPI - Version](https://img.shields.io/pypi/v/terml)]() [![Total Downloads](https://static.pepy.tech/badge/terml)]()

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

![image](https://github.com/s3rgeym/terml/assets/12753171/b3681eff-dff3-4964-a6fe-0329a4829156)


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
