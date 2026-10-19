from __future__ import annotations

import difflib
import re

from app.models import Severity


NUMERIC_RE = re.compile(r"\d")


def unified_diff(old: str, new: str) -> str:
    lines = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        lineterm="",
        n=2,
    )
    text = "\n".join(lines)
    truncated = text.split("\n")[:40]
    return "\n".join(truncated)


def summarize(diff: str) -> str:
    added = [l[1:].strip() for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]
    removed = [l[1:].strip() for l in diff.split("\n") if l.startswith("-") and not l.startswith("---")]
    if added and removed:
        return f'Changed: "{removed[0]}" -> "{added[0]}"'[:120]
    if added:
        return f'Added: "{added[0]}"'[:120]
    if removed:
        return f'Removed: "{removed[0]}"'[:120]
    return "Content changed"


def classify_severity(diff: str) -> Severity:
    added = [l for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++")]
    removed = [l for l in diff.split("\n") if l.startswith("-") and not l.startswith("---")]
    changed_text = "\n".join(added + removed)

    if NUMERIC_RE.search(changed_text):
        return "high"

    for line in added:
        body = line[1:].strip()
        if body and (body.isupper() or body.endswith(":")):
            return "medium"

    return "low"