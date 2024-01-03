# terminal-markup

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/terminal-markup)]() [![PyPI - Version](https://img.shields.io/pypi/v/terminal-markup)]() [![Total Downloads](https://static.pepy.tech/badge/terminal-markup)]()

Render Markup to Terminal.

Inspired by [tml](https://github.com/liamg/tml).

Pros:

* Faster than alternatvies like `rich`.
* Supports background color and hex-colors.
* Null-dependency.

Install:

```bash
pip install terminal-markup
poetry add terminal-markup
```

After install you can use comand `terminal-markup`.

## Examples

```python
from terminal_markup import render

# let's render bricks
print(render("[b][color=#f70000 background=yellow] WARNING [/color]:[/b] [purple]Life leads to [i blue underline]Death[/i].[/purple]"))
```

![image](https://github.com/s3rgeym/terminal-markup/assets/12753171/b3681eff-dff3-4964-a6fe-0329a4829156)

> `\[` - escaped `[`.

## Tags

| Tag | Description |
| --- | --- |
| `b`, `bold` | Bold text |
| `i`, `em` | Italic text |
| `u` | Underline text |
| `blink` | -- |
| `dim` | Dimmed color |
| `rev` | Reversed foreground and background colors |
| `[color=<color>]`, `<color name>` | Set foreground color |

Non-existent tags do not cause errors.

## Common attributes

| Attribute | Description |
| -- | -- |
| `<color name>`, `color=<color>` | Set foreground color |
| `background=<color>` | Set background color |
| `{bold\|italic\|underline\|dim\|reversed\|blink}[={no\|off\|false\|0\|...}]` | Set style |

Unknown attributes are ignored.

## Colors

Color names: black, maroon, green, olive, navy, purple, teal, silver, grey, red, lime, yellow, blue, fuchsia, aqua, white (first 16 colors from [here](https://ss64.com/bash/syntax-colors.html)). Also supported HEX-codes like `#87CEEB`.

## Case Insensetive

Tag names, attributes and color names are case insensetive.
