from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EconCommand:
    """A registered economics research command."""

    name: str
    stage: str
    responsibility: str
    source_skill: str
    template_hint: str = ''


@dataclass(frozen=True)
class EconTool:
    """A registered economics research tool."""

    name: str
    kind: str  # 'executor' | 'checker' | 'generator'
    responsibility: str


@dataclass(frozen=True)
class PipelineStage:
    """One stage of the research pipeline."""

    name: str
    description: str
    skill_sources: tuple[str, ...]
    prerequisites: tuple[str, ...]
    commands: tuple[str, ...]
    tools: tuple[str, ...]


@dataclass(frozen=True)
class RoutedMatch:
    """A prompt-to-command/tool match with score."""

    kind: str  # 'command' or 'tool'
    name: str
    stage: str
    score: int


@dataclass(frozen=True)
class CommandExecution:
    """Result of executing an econ command."""

    name: str
    prompt: str
    message: str


@dataclass(frozen=True)
class ToolExecution:
    """Result of executing an econ tool."""

    name: str
    payload: str
    message: str


@dataclass(frozen=True)
class UsageSummary:
    """Token usage tracking."""

    input_tokens: int = 0
    output_tokens: int = 0

    def add_turn(self, inp: int = 0, out: int = 0) -> UsageSummary:
        return UsageSummary(self.input_tokens + inp, self.output_tokens + out)


@dataclass(frozen=True)
class PermissionDenial:
    """A denied tool access record."""

    tool_name: str
    reason: str


@dataclass(frozen=True)
class TurnResult:
    """Result of a single query engine turn."""

    prompt: str
    output: str
    matched_commands: tuple[str, ...]
    matched_tools: tuple[str, ...]
    permission_denials: tuple[PermissionDenial, ...]
    usage: UsageSummary
    stop_reason: str


@dataclass(frozen=True)
class TemplateEntry:
    """A code template metadata entry."""

    name: str
    lang: str  # 'stata' | 'r' | 'python'
    description: str
    path: str


@dataclass(frozen=True)
class IntegrityWarning:
    """An academic integrity concern."""

    level: str  # 'error' | 'warning' | 'info'
    category: str  # 'fabrication' | 'citation' | 'causality' | 'verification'
    message: str


@dataclass(frozen=True)
class StoredSession:
    """A persisted research session."""

    session_id: str
    project_name: str
    current_stage: str
    messages: tuple[str, ...]
    responses: tuple[str, ...] = ()   # API 返回的完整内容
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class ResearchContext:
    """Research project directory context."""

    project_root: str
    data_dir: str
    code_dir: str
    output_dir: str
    paper_dir: str
    has_stata: bool = False
    has_r: bool = False
    has_python: bool = False
    stata_file_count: int = 0
    r_file_count: int = 0
    python_file_count: int = 0
    tex_file_count: int = 0
