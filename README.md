# terminal-markup

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/terminal-markup)]() [![PyPI - Version](https://img.shields.io/pypi/v/terminal-markup)]() [![Total Downloads](https://static.pepy.tech/badge/terminal-markup)]()

Converts Markup to Terminal ANSI Escape Codes.

Inspired by [tml](https://github.com/liamg/tml).

Pros:

* Faster than alterntavies like `rich`.
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
from terminal_markup import convert

print(convert("[b][color=#f70000 background=yellow] WARNING [/color]:[/b] [magenta]Life leads to [i blue underline]Death[/i].[/magenta]"))
```

![image](https://github.com/s3rgeym/terminal-markup/assets/12753171/b3681eff-dff3-4964-a6fe-0329a4829156)

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
| `<color name>`, `color=<color>` | Set foreground color |
| `background=<color>` | Set background color |
| `{bold\|italic\|underline}[={no\|off\|false\|0\|...}]` | Set text style |

Unknown attributes are ignored.

## Colors

Color name: `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`. Also supported HEX-codes like `#deadbeef`.
