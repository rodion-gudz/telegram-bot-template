import html
from typing import Any


def escape(txt: Any):
    return html.escape(str(txt))
