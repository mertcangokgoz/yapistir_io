import logging
import os

import markdown
from django.template.defaultfilters import escape
from django.utils.safestring import mark_safe
from docutils.core import publish_parts
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.styles import get_all_styles
from pygments.util import ClassNotFound
from pygments_lexer_solidity import SolidityLexer

logger = logging.getLogger(__name__)


class NakedHtmlFormatter(HtmlFormatter):
    def wrap(self, source):  # noqa
        return self._wrap_code(source)

    def _wrap_code(self, source):  # noqa
        yield from source


def pygmentize(code_string: str, lexer_name: str = "_code") -> object:
    if lexer_name == "_code":
        return "\n".join(
            [
                f'<span class="plain">{escape(l) or "&#8203;"}</span>'
                for l in code_string.splitlines()
            ]
        )

    if lexer_name == "_text":
        return code_string
    if lexer_name == "_markdown":
        extensions = (
            "pymdownx.betterem",
            "pymdownx.superfences",
            "pymdownx.arithmatex",
            "pymdownx.emoji",
            "pymdownx.tasklist",
            "pymdownx.striphtml",
            "pymdownx.extra",
            "pymdownx.smartsymbols",
            "pymdownx.mark",
            "pymdownx.inlinehilite",
            "pymdownx.escapeall",
            "markdown.extensions.footnotes",
            "markdown.extensions.attr_list",
            "markdown.extensions.def_list",
            "markdown.extensions.tables",
            "markdown.extensions.abbr",
            "fenced_code",
            "footnotes",
            "toc",
        )
        return mark_safe(
            markdown.markdown(
                code_string,
                extensions=extensions,
                output_format="html",
                tab_length=4
            )
        )
    if lexer_name == "_rst":
        rst_part_name = "html_body"
        publish_args = {
            "writer_name": "html5_polyglot", "settings_overrides": {
                "raw_enabled": False,
                "file_insertion_enabled": False,
                "halt_level": 5,
                "report_level": 2,
                "warning_stream": os.devnull,
            }, "source": code_string
        }

        parts = publish_parts(**publish_args)
        return mark_safe(parts[rst_part_name])
    if lexer_name == "solidity":
        return SolidityLexer()

    lexer = None
    try:
        lexer = get_lexer_by_name(lexer_name, stripall=True)
    except ClassNotFound:
        logger.exception("Could not find lexer for %s", lexer_name)
    if not lexer:
        lexer = "text"

    formatter = NakedHtmlFormatter(linenos='table', anchorlinenos=True, lineanchors='line')

    return highlight(code_string, lexer, formatter)


LEXERS = [item for item in get_all_lexers() if item[1]]
TEXT_CHOICES = sorted(
    [
        ("_markdown", "Markdown"),
        ("_text", "Text"),
        ("_rst", "reStructuredText"),
        ("_code", "Plain Code")
    ]
)
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])

LEXER_CHOICES = (
    ("Text", TEXT_CHOICES),
    ("Code", LANGUAGE_CHOICES),
)

LEXER_KEYS = TEXT_CHOICES + LANGUAGE_CHOICES
