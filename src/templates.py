from __future__ import annotations

from pathlib import Path

from .models import TemplateEntry

TEMPLATES_DIR = Path(__file__).resolve().parent / 'reference_data' / 'templates'

# Template metadata registry
_TEMPLATES: list[TemplateEntry] = [
    # Stata templates
    TemplateEntry('reghdfe-main', 'stata', 'Main regression table with reghdfe + estout', 'stata/reghdfe_main.do'),
    TemplateEntry('event-study', 'stata', 'Event study estimation with leads/lags and coefplot', 'stata/event_study.do'),
    TemplateEntry('balance-table', 'stata', 'Treatment-control balance table using iebaltab', 'stata/balance_table.do'),
    TemplateEntry('summary-stats', 'stata', 'Summary statistics table for paper', 'stata/summary_stats.do'),
    TemplateEntry('did', 'stata', 'Difference-in-differences with parallel trends test', 'stata/did.do'),
    TemplateEntry('dofile-header', 'stata', 'Standardized do-file header with globals and paths', 'stata/dofile_header.do'),
    # R templates
    TemplateEntry('fixest-main', 'r', 'Main regression table with fixest + etable', 'r/fixest_main.R'),
    TemplateEntry('honest-did', 'r', 'HonestDiD sensitivity analysis (Rambachan & Roth 2023)', 'r/honest_did.R'),
    TemplateEntry('cs-did', 'r', 'Callaway & Sant\'Anna staggered DiD', 'r/cs_did.R'),
    # Python templates
    TemplateEntry('romano-wolf', 'python', 'Romano-Wolf multiple hypothesis testing correction', 'python/romano_wolf.py'),
    TemplateEntry('panel-reg', 'python', 'Panel regression with linearmodels', 'python/panel_reg.py'),
]


def get_template(name: str, lang: str | None = None) -> str | None:
    """Return a code template's content by name and optional language."""
    for entry in _TEMPLATES:
        if entry.name == name and (lang is None or entry.lang == lang):
            path = TEMPLATES_DIR / entry.path
            if path.exists():
                return path.read_text(encoding='utf-8')
            return f'[Template placeholder: {entry.path}]\n{entry.description}'
    return None


def get_template_entry(name: str, lang: str | None = None) -> TemplateEntry | None:
    for entry in _TEMPLATES:
        if entry.name == name and (lang is None or entry.lang == lang):
            return entry
    return None


def list_templates(lang: str | None = None) -> list[TemplateEntry]:
    if lang is None:
        return list(_TEMPLATES)
    return [t for t in _TEMPLATES if t.lang == lang]


def render_template_index(lang: str | None = None) -> str:
    templates = list_templates(lang)
    lines = [f'# Code Templates ({len(templates)} available)', '']
    current_lang = ''
    for t in templates:
        if t.lang != current_lang:
            current_lang = t.lang
            lines.append(f'\n## {current_lang.upper()}')
        lines.append(f'- **{t.name}** — {t.description}')
    return '\n'.join(lines)
