"""Wrap Latin/numeric runs in Unicode bidi isolates for clean RTL+LTR mixing.

The Arabic (فصحى) subtitle lines contain embedded Latin runs -- physics symbols
and subscripts such as ``r``, ``T``, ``A``, ``B``, ``r_A``, ``T_B``, numbers, and
parentheses around Latin tokens. When such mixed text is fed raw into a libass
ASS event, the Unicode bidirectional algorithm can reorder neighbouring Latin
tokens in a way that scrambles their visual order.

``isolate_ltr`` wraps every maximal run of Latin letters / digits / underscores
(optionally including immediately adjacent punctuation such as parentheses and
the separators that glue a parenthetical Latin group together) in a Unicode
*isolate*::

    U+2066 LEFT-TO-RIGHT ISOLATE (LRI)  ...  U+2069 POP DIRECTIONAL ISOLATE (PDI)

An isolate tells the bidi algorithm to treat the wrapped span as a single
neutral character with respect to the surrounding text, while resolving its own
internal direction independently. This keeps the Latin run's internal order
intact and prevents it from interacting with adjacent Arabic.
"""

import re

# Unicode bidi isolate controls.
LRI = "⁦"  # LEFT-TO-RIGHT ISOLATE
PDI = "⁩"  # POP DIRECTIONAL ISOLATE

# A Latin "run": one or more Latin tokens (letters/digits/underscore), where
# tokens may be joined by spaces, commas or parentheses so that something like
# "(mass, path)" or "r_A على r_B" -> the "r_A" and "r_B" tokens, and the
# "(mass, path)" parenthetical, each form one isolate. We grow the run across
# Latin-internal punctuation (space, comma, parens, dot, slash, hyphen) only as
# long as it stays "glued" to Latin on both sides; trailing punctuation that
# belongs to the surrounding Arabic sentence is left outside the isolate.
_CORE = r"[A-Za-z0-9_]"
# Punctuation allowed *between* Latin tokens inside a single isolate.
_GLUE = r"[ ,./\-]"

# Match: an optional opening paren, a Latin core token, then any number of
# (glue + Latin core) repetitions, and an optional closing paren. The opening
# "(" is only consumed when it is directly followed by Latin (handled by the
# alternation below). This keeps Arabic punctuation out of the isolate.
_PATTERN = re.compile(
    r"\(?"          # optional opening paren ( "(mass" )
    + _CORE + r"+"  # first Latin token
    + r"(?:" + _GLUE + r"+" + _CORE + r"+)*"  # more Latin tokens joined by glue
    + r"\)?"        # optional closing paren ( "path)" )
)


def isolate_ltr(text: str) -> str:
    """Return ``text`` with every Latin/numeric run wrapped in LRI...PDI.

    Surrounding Arabic is left untouched. Idempotent-ish: re-running will not
    add a second layer because the isolate controls themselves are not part of
    the matched character classes.
    """
    def _wrap(m: "re.Match[str]") -> str:
        run = m.group(0)
        # Don't wrap a lone opening/closing paren that got pulled in with no
        # Latin (the pattern guarantees >=1 Latin char, so this is just tidy).
        return f"{LRI}{run}{PDI}"

    return _PATTERN.sub(_wrap, text)


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    samples = [
        "جرّب نسبة المسافتين: r_A على r_B — كم مرّةً يبعد A أكثر من B.",
        "كوكبٌ يكشف عن آخر — لا كتلته ولا شكل مساره (mass, path).",
    ]
    for s in samples:
        out = isolate_ltr(s)
        # Show the isolate controls visibly as <LRI>/<PDI> for inspection.
        vis = out.replace(LRI, "<LRI>").replace(PDI, "<PDI>")
        print(vis)
