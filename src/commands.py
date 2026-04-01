from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import CommandExecution, EconCommand

SNAPSHOT_PATH = Path(__file__).resolve().parent / 'reference_data' / 'commands_snapshot.json'


@lru_cache(maxsize=1)
def load_command_snapshot() -> tuple[EconCommand, ...]:
    raw = json.loads(SNAPSHOT_PATH.read_text(encoding='utf-8'))
    return tuple(
        EconCommand(
            name=entry['name'],
            stage=entry['stage'],
            responsibility=entry['responsibility'],
            source_skill=entry['source_skill'],
            template_hint=entry.get('template_hint', ''),
        )
        for entry in raw
    )


ECON_COMMANDS = load_command_snapshot()


def get_command(name: str) -> EconCommand | None:
    for cmd in ECON_COMMANDS:
        if cmd.name == name:
            return cmd
    return None


def get_commands(stage: str | None = None) -> tuple[EconCommand, ...]:
    if stage is None:
        return ECON_COMMANDS
    return tuple(cmd for cmd in ECON_COMMANDS if cmd.stage == stage)


def find_commands(query: str, limit: int = 20) -> list[EconCommand]:
    query_lower = query.lower()
    scored: list[tuple[int, EconCommand]] = []
    for cmd in ECON_COMMANDS:
        score = 0
        haystack = f'{cmd.name} {cmd.responsibility} {cmd.stage}'.lower()
        for token in query_lower.split():
            if token in haystack:
                score += 1
        if score > 0:
            scored.append((score, cmd))
    scored.sort(key=lambda pair: (-pair[0], pair[1].name))
    return [cmd for _, cmd in scored[:limit]]


def execute_command(name: str, prompt: str) -> CommandExecution:
    cmd = get_command(name)
    if cmd is None:
        return CommandExecution(
            name=name,
            prompt=prompt,
            message=f'Unknown command: {name}',
        )
    return CommandExecution(
        name=name,
        prompt=prompt,
        message=f'[{cmd.stage}] {cmd.name}: {cmd.responsibility} (skill: {cmd.source_skill})',
    )


def render_command_index(limit: int = 20, query: str | None = None, stage: str | None = None) -> str:
    if query:
        commands = find_commands(query, limit)
    elif stage:
        commands = list(get_commands(stage))[:limit]
    else:
        commands = list(ECON_COMMANDS[:limit])

    lines = [f'# Econ Commands ({len(commands)} shown)', '']
    current_stage = ''
    for cmd in commands:
        if cmd.stage != current_stage:
            current_stage = cmd.stage
            lines.append(f'\n## {current_stage.upper()}')
        lines.append(f'- **{cmd.name}** — {cmd.responsibility}')
        if cmd.template_hint:
            lines.append(f'  template: `{cmd.template_hint}`')
    return '\n'.join(lines)
