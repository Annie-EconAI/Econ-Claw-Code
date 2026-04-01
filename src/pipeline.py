from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import PipelineStage

STAGES_PATH = Path(__file__).resolve().parent / 'reference_data' / 'pipeline_stages.json'

STAGE_ORDER = ('data', 'analysis', 'viz', 'write', 'review', 'submit')


@lru_cache(maxsize=1)
def load_pipeline_stages() -> tuple[PipelineStage, ...]:
    raw = json.loads(STAGES_PATH.read_text(encoding='utf-8'))
    return tuple(
        PipelineStage(
            name=entry['name'],
            description=entry['description'],
            skill_sources=tuple(entry['skill_sources']),
            prerequisites=tuple(entry['prerequisites']),
            commands=(),
            tools=(),
        )
        for entry in raw
    )


PIPELINE_STAGES = load_pipeline_stages()

# Build keyword lookup from pipeline_stages.json
@lru_cache(maxsize=1)
def _stage_keywords() -> dict[str, list[str]]:
    raw = json.loads(STAGES_PATH.read_text(encoding='utf-8'))
    return {entry['name']: entry.get('keywords', []) for entry in raw}


def get_stage(name: str) -> PipelineStage | None:
    for stage in PIPELINE_STAGES:
        if stage.name == name:
            return stage
    return None


def detect_stage(prompt: str) -> str:
    """Classify a prompt into a pipeline stage using keyword matching.

    Returns the best-matching stage name, or 'analysis' as the default.
    """
    prompt_lower = prompt.lower()
    keywords = _stage_keywords()
    best_stage = 'analysis'
    best_score = 0

    for stage_name, kws in keywords.items():
        score = sum(1 for kw in kws if kw in prompt_lower)
        if score > best_score:
            best_score = score
            best_stage = stage_name

    return best_stage


def render_pipeline() -> str:
    lines = ['# Research Pipeline', '']
    for i, stage in enumerate(PIPELINE_STAGES, 1):
        prereqs = ', '.join(stage.prerequisites) if stage.prerequisites else 'none'
        skills = ', '.join(stage.skill_sources)
        lines.append(f'## Stage {i}: {stage.name.upper()}')
        lines.append(f'{stage.description}')
        lines.append(f'- Prerequisites: {prereqs}')
        lines.append(f'- Skills: {skills}')
        lines.append('')
    return '\n'.join(lines)
