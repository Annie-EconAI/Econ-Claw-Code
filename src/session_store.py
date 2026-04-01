from __future__ import annotations

import json
from pathlib import Path

from .models import StoredSession

DEFAULT_SESSION_DIR = '.econ_sessions'


def save_session(session: StoredSession, directory: str | None = None) -> Path:
    """Persist a research session to JSON."""
    base = Path(directory) if directory else Path.cwd() / DEFAULT_SESSION_DIR
    base.mkdir(parents=True, exist_ok=True)
    path = base / f'{session.session_id}.json'
    data = {
        'session_id': session.session_id,
        'project_name': session.project_name,
        'current_stage': session.current_stage,
        'messages': list(session.messages),
        'responses': list(session.responses),
        'input_tokens': session.input_tokens,
        'output_tokens': session.output_tokens,
    }
    path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    return path


def load_session(session_id: str, directory: str | None = None) -> StoredSession:
    """Load a persisted research session."""
    base = Path(directory) if directory else Path.cwd() / DEFAULT_SESSION_DIR
    path = base / f'{session_id}.json'
    data = json.loads(path.read_text(encoding='utf-8'))
    return StoredSession(
        session_id=data['session_id'],
        project_name=data.get('project_name', ''),
        current_stage=data.get('current_stage', 'data'),
        messages=tuple(data.get('messages', ())),
        responses=tuple(data.get('responses', ())),
        input_tokens=data.get('input_tokens', 0),
        output_tokens=data.get('output_tokens', 0),
    )


def list_sessions(directory: str | None = None) -> list[str]:
    """List all saved session IDs."""
    base = Path(directory) if directory else Path.cwd() / DEFAULT_SESSION_DIR
    if not base.exists():
        return []
    return [p.stem for p in sorted(base.glob('*.json'))]
