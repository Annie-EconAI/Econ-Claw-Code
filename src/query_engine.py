from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generator
from uuid import uuid4

from .models import PermissionDenial, TurnResult, UsageSummary
from .pipeline import detect_stage


@dataclass(frozen=True)
class EconEngineConfig:
    max_turns: int = 8
    max_budget_tokens: int = 2000
    compact_after_turns: int = 12


@dataclass
class EconQueryEngine:
    """Multi-turn research session engine.

    Multi-turn research session engine for economics research.
    """

    config: EconEngineConfig = field(default_factory=EconEngineConfig)
    session_id: str = field(default_factory=lambda: uuid4().hex)
    project_name: str = ''
    mutable_messages: list[str] = field(default_factory=list)
    permission_denials: list[PermissionDenial] = field(default_factory=list)
    total_usage: UsageSummary = field(default_factory=UsageSummary)

    def submit_message(
        self,
        prompt: str,
        matched_commands: tuple[str, ...] = (),
        matched_tools: tuple[str, ...] = (),
        denied_tools: tuple[PermissionDenial, ...] = (),
    ) -> TurnResult:
        if len(self.mutable_messages) >= self.config.max_turns:
            return TurnResult(
                prompt=prompt,
                output=f'Max turns reached ({self.config.max_turns}). Session: {self.session_id}',
                matched_commands=matched_commands,
                matched_tools=matched_tools,
                permission_denials=denied_tools,
                usage=self.total_usage,
                stop_reason='max_turns_reached',
            )

        detected_stage = detect_stage(prompt)

        if denied_tools:
            self.permission_denials.extend(denied_tools)

        summary_lines = [
            f'Session: {self.session_id}',
            f'Turn: {len(self.mutable_messages) + 1}/{self.config.max_turns}',
            f'Detected stage: {detected_stage}',
        ]
        if matched_commands:
            summary_lines.append(f'Commands: {", ".join(matched_commands)}')
        if matched_tools:
            summary_lines.append(f'Tools: {", ".join(matched_tools)}')
        if denied_tools:
            summary_lines.append(f'Denied: {", ".join(d.tool_name for d in denied_tools)}')

        output = '\n'.join(summary_lines)
        self.mutable_messages.append(f'[{detected_stage}] {prompt}')

        inp_tokens = len(prompt.split()) * 2
        out_tokens = len(output.split()) * 2
        self.total_usage = self.total_usage.add_turn(inp_tokens, out_tokens)

        return TurnResult(
            prompt=prompt,
            output=output,
            matched_commands=matched_commands,
            matched_tools=matched_tools,
            permission_denials=denied_tools,
            usage=self.total_usage,
            stop_reason='completed',
        )

    def stream_submit_message(
        self,
        prompt: str,
        matched_commands: tuple[str, ...] = (),
        matched_tools: tuple[str, ...] = (),
    ) -> Generator[dict[str, object], None, None]:
        yield {'type': 'message_start', 'session_id': self.session_id}

        if matched_commands:
            yield {'type': 'command_match', 'commands': matched_commands}
        if matched_tools:
            yield {'type': 'tool_match', 'tools': matched_tools}

        result = self.submit_message(prompt, matched_commands, matched_tools)

        yield {'type': 'message_delta', 'output': result.output}
        yield {
            'type': 'message_stop',
            'stop_reason': result.stop_reason,
            'usage': {'input': result.usage.input_tokens, 'output': result.usage.output_tokens},
        }

    def compact_messages_if_needed(self) -> None:
        if len(self.mutable_messages) > self.config.compact_after_turns:
            keep = self.config.compact_after_turns // 2
            self.mutable_messages = self.mutable_messages[-keep:]

    def render_summary(self) -> str:
        lines = [
            '# Research Session Summary',
            '',
            f'- Session ID: {self.session_id}',
            f'- Project: {self.project_name or "(unnamed)"}',
            f'- Turns: {len(self.mutable_messages)}',
            f'- Token usage: {self.total_usage.input_tokens} in / {self.total_usage.output_tokens} out',
            '',
            '## Message History',
        ]
        for i, msg in enumerate(self.mutable_messages, 1):
            lines.append(f'{i}. {msg}')
        if self.permission_denials:
            lines.extend(['', '## Permission Denials'])
            for denial in self.permission_denials:
                lines.append(f'- {denial.tool_name}: {denial.reason}')
        return '\n'.join(lines)
