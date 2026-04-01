from __future__ import annotations

from .commands import ECON_COMMANDS, execute_command, find_commands
from .models import CommandExecution, RoutedMatch, ToolExecution
from .pipeline import detect_stage
from .tools import ECON_TOOLS, execute_tool, find_tools


class EconRuntime:
    """Routes research prompts to economics commands and tools."""

    def route_prompt(self, prompt: str, limit: int = 5) -> list[RoutedMatch]:
        """Route a prompt to matching econ commands/tools.

        Uses token-based scoring plus a stage-aware boost:
        if the prompt maps to a detected stage, commands/tools in that stage
        get an extra score bonus.
        """
        detected_stage = detect_stage(prompt)
        tokens = _tokenize(prompt)
        matches: list[RoutedMatch] = []

        for cmd in ECON_COMMANDS:
            score = _score(tokens, cmd.name, cmd.responsibility)
            if cmd.stage == detected_stage:
                score += 2  # stage-aware boost
            if score > 0:
                matches.append(RoutedMatch(
                    kind='command',
                    name=cmd.name,
                    stage=cmd.stage,
                    score=score,
                ))

        for tool in ECON_TOOLS:
            score = _score(tokens, tool.name, tool.responsibility)
            if score > 0:
                matches.append(RoutedMatch(
                    kind='tool',
                    name=tool.name,
                    stage=tool.kind,
                    score=score,
                ))

        matches.sort(key=lambda m: (-m.score, m.kind, m.name))
        return matches[:limit]

    def execute_matches(
        self,
        matches: list[RoutedMatch],
        prompt: str,
    ) -> tuple[list[CommandExecution], list[ToolExecution]]:
        """Execute all matched commands and tools."""
        cmd_results: list[CommandExecution] = []
        tool_results: list[ToolExecution] = []
        for match in matches:
            if match.kind == 'command':
                cmd_results.append(execute_command(match.name, prompt))
            else:
                tool_results.append(execute_tool(match.name, prompt))
        return cmd_results, tool_results

    def route_and_execute(
        self,
        prompt: str,
        limit: int = 5,
    ) -> str:
        """Route prompt, execute matches, return formatted report."""
        detected_stage = detect_stage(prompt)
        matches = self.route_prompt(prompt, limit)
        cmd_results, tool_results = self.execute_matches(matches, prompt)

        lines = [
            '# Routing Report',
            '',
            f'**Prompt:** {prompt}',
            f'**Detected stage:** {detected_stage}',
            '',
            '## Matches',
        ]
        if matches:
            for m in matches:
                lines.append(f'- [{m.kind}] **{m.name}** (stage={m.stage}, score={m.score})')
        else:
            lines.append('- No matches found')

        if cmd_results:
            lines.extend(['', '## Command Execution'])
            for cr in cmd_results:
                lines.append(f'- {cr.message}')

        if tool_results:
            lines.extend(['', '## Tool Execution'])
            for tr in tool_results:
                lines.append(f'- {tr.message}')

        return '\n'.join(lines)


def _tokenize(text: str) -> list[str]:
    """Split text into lowercase tokens, splitting on whitespace, /, -."""
    tokens: list[str] = []
    for word in text.lower().replace('/', ' ').replace('-', ' ').split():
        stripped = word.strip('.,;:!?()[]{}"\'"')
        if stripped:
            tokens.append(stripped)
    return tokens


def _score(tokens: list[str], name: str, responsibility: str) -> int:
    """Score how well tokens match a name and responsibility string."""
    haystack = f'{name} {responsibility}'.lower().replace('-', ' ')
    return sum(1 for token in tokens if token in haystack)
