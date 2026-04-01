from __future__ import annotations

from pathlib import Path

from .models import ResearchContext


def build_research_context(base: Path | None = None) -> ResearchContext:
    """Detect research project structure from a base directory."""
    root = base or Path.cwd()

    # Common economics project directory conventions
    data_dir = _find_dir(root, ('data', 'rawdata', 'raw_data', 'Data'))
    code_dir = _find_dir(root, ('code', 'do', 'dofiles', 'scripts', 'Code', 'analysis'))
    output_dir = _find_dir(root, ('output', 'results', 'tables', 'figures', 'Output'))
    paper_dir = _find_dir(root, ('paper', 'draft', 'tex', 'manuscript', 'Paper'))

    stata_files = list(root.rglob('*.do')) + list(root.rglob('*.ado'))
    r_files = list(root.rglob('*.R')) + list(root.rglob('*.Rmd'))
    python_files = list(root.rglob('*.py'))
    tex_files = list(root.rglob('*.tex'))

    return ResearchContext(
        project_root=str(root),
        data_dir=str(data_dir),
        code_dir=str(code_dir),
        output_dir=str(output_dir),
        paper_dir=str(paper_dir),
        has_stata=len(stata_files) > 0,
        has_r=len(r_files) > 0,
        has_python=len(python_files) > 0,
        stata_file_count=len(stata_files),
        r_file_count=len(r_files),
        python_file_count=len(python_files),
        tex_file_count=len(tex_files),
    )


def render_context(ctx: ResearchContext) -> str:
    lines = [
        '# Research Project Context',
        '',
        f'- Root: {ctx.project_root}',
        f'- Data: {ctx.data_dir}',
        f'- Code: {ctx.code_dir}',
        f'- Output: {ctx.output_dir}',
        f'- Paper: {ctx.paper_dir}',
        '',
        '## File Counts',
        f'- Stata (.do/.ado): {ctx.stata_file_count}',
        f'- R (.R/.Rmd): {ctx.r_file_count}',
        f'- Python (.py): {ctx.python_file_count}',
        f'- LaTeX (.tex): {ctx.tex_file_count}',
    ]
    langs = []
    if ctx.has_stata:
        langs.append('Stata')
    if ctx.has_r:
        langs.append('R')
    if ctx.has_python:
        langs.append('Python')
    if langs:
        lines.append(f'\nDetected languages: {", ".join(langs)}')
    return '\n'.join(lines)


def _find_dir(root: Path, candidates: tuple[str, ...]) -> Path:
    for name in candidates:
        candidate = root / name
        if candidate.is_dir():
            return candidate
    return root
