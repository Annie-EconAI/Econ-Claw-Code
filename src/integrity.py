from __future__ import annotations

import re

from .models import IntegrityWarning

# Patterns that suggest potential integrity issues
_FABRICATION_PATTERNS = [
    (r'\b(?:I made up|fabricated|invented)\b', 'fabrication', 'Possible fabrication language detected'),
    (r'\bplaceholder\b', 'fabrication', 'Placeholder content detected — replace with real data'),
    (r'\bXXX\b|\bTODO\b|\b\?\?\?\b', 'fabrication', 'Unresolved placeholder found'),
]

_CAUSALITY_PATTERNS = [
    (r'\b(?:proves? that|caused? by|causal effect)\b(?!.*(?:instrument|exogenous|random))',
     'causality', 'Causal language used — ensure identification strategy supports this claim'),
    (r'\bsignificant\b(?!.*(?:statistically|economically|at the))',
     'causality', 'Ambiguous use of "significant" — specify statistically or economically'),
]

_CITATION_PATTERNS = [
    (r'\(\d{4}\)(?!.*\\cite)',
     'citation', 'Year in parentheses without \\cite — may be a missing citation'),
    (r'(?:et al\.,? \d{4})',
     'citation', 'In-text citation detected — verify it exists in your .bib file'),
]


def check_integrity(text: str) -> list[IntegrityWarning]:
    """Scan text for academic integrity concerns.

    Returns a list of warnings ordered by severity (errors first).
    """
    warnings: list[IntegrityWarning] = []

    for pattern, category, message in _FABRICATION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append(IntegrityWarning(
                level='error',
                category=category,
                message=message,
            ))

    for pattern, category, message in _CAUSALITY_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            warnings.append(IntegrityWarning(
                level='warning',
                category=category,
                message=message,
            ))

    for pattern, category, message in _CITATION_PATTERNS:
        if re.search(pattern, text):
            warnings.append(IntegrityWarning(
                level='info',
                category=category,
                message=message,
            ))

    # Sort: errors first, then warnings, then info
    level_order = {'error': 0, 'warning': 1, 'info': 2}
    warnings.sort(key=lambda w: level_order.get(w.level, 3))
    return warnings


def render_integrity_report(warnings: list[IntegrityWarning]) -> str:
    if not warnings:
        return 'Integrity check passed — no issues found.'

    lines = [f'# Integrity Check ({len(warnings)} issues)', '']
    for w in warnings:
        icon = {'error': '[ERROR]', 'warning': '[WARN]', 'info': '[INFO]'}.get(w.level, '[?]')
        lines.append(f'{icon} [{w.category}] {w.message}')
    return '\n'.join(lines)
