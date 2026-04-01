from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import EconTool, ToolExecution

SNAPSHOT_PATH = Path(__file__).resolve().parent / 'reference_data' / 'tools_snapshot.json'


@lru_cache(maxsize=1)
def load_tool_snapshot() -> tuple[EconTool, ...]:
    raw = json.loads(SNAPSHOT_PATH.read_text(encoding='utf-8'))
    return tuple(
        EconTool(
            name=entry['name'],
            kind=entry['kind'],
            responsibility=entry['responsibility'],
        )
        for entry in raw
    )


ECON_TOOLS = load_tool_snapshot()


def get_tool(name: str) -> EconTool | None:
    for tool in ECON_TOOLS:
        if tool.name == name:
            return tool
    return None


def get_tools(kind: str | None = None) -> tuple[EconTool, ...]:
    if kind is None:
        return ECON_TOOLS
    return tuple(t for t in ECON_TOOLS if t.kind == kind)


def find_tools(query: str, limit: int = 20) -> list[EconTool]:
    query_lower = query.lower()
    scored: list[tuple[int, EconTool]] = []
    for tool in ECON_TOOLS:
        score = 0
        haystack = f'{tool.name} {tool.responsibility} {tool.kind}'.lower()
        for token in query_lower.split():
            if token in haystack:
                score += 1
        if score > 0:
            scored.append((score, tool))
    scored.sort(key=lambda pair: (-pair[0], pair[1].name))
    return [tool for _, tool in scored[:limit]]


def execute_tool(name: str, payload: str) -> ToolExecution:
    tool = get_tool(name)
    if tool is None:
        return ToolExecution(
            name=name,
            payload=payload,
            message=f'Unknown tool: {name}',
        )
    return ToolExecution(
        name=name,
        payload=payload,
        message=f'[{tool.kind}] {tool.name}: {tool.responsibility}',
    )


def render_tool_index(limit: int = 20, query: str | None = None, kind: str | None = None) -> str:
    if query:
        tools = find_tools(query, limit)
    elif kind:
        tools = list(get_tools(kind))[:limit]
    else:
        tools = list(ECON_TOOLS[:limit])

    lines = [f'# Econ Tools ({len(tools)} shown)', '']
    current_kind = ''
    for tool in tools:
        if tool.kind != current_kind:
            current_kind = tool.kind
            lines.append(f'\n## {current_kind.upper()}')
        lines.append(f'- **{tool.name}** — {tool.responsibility}')
    return '\n'.join(lines)
