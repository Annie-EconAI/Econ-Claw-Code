from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .commands import execute_command, get_command, render_command_index
from .context import build_research_context, render_context
from .integrity import check_integrity, render_integrity_report
from .models import StoredSession
from .pipeline import detect_stage, render_pipeline
from .query_engine import EconEngineConfig, EconQueryEngine
from .runtime import EconRuntime
from .session_store import list_sessions, load_session, save_session
from .templates import get_template, render_template_index
from .tools import execute_tool, get_tool, render_tool_index


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='econ-claw',
        description='CLI tool for economics and social science empirical research',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Pipeline overview
    subparsers.add_parser('pipeline', help='show the 6-stage research pipeline')

    # Stage detection
    stage_p = subparsers.add_parser('stage', help='detect pipeline stage for a prompt')
    stage_p.add_argument('prompt')

    # Prompt routing
    route_p = subparsers.add_parser('route', help='route a research prompt to matching commands/tools')
    route_p.add_argument('prompt')
    route_p.add_argument('--limit', type=int, default=5)

    # Command listing
    cmd_p = subparsers.add_parser('commands', help='list economics commands')
    cmd_p.add_argument('--stage', choices=['data', 'analysis', 'viz', 'write', 'review', 'submit'])
    cmd_p.add_argument('--query')
    cmd_p.add_argument('--limit', type=int, default=40)

    # Tool listing
    tool_p = subparsers.add_parser('tools', help='list economics tools')
    tool_p.add_argument('--kind', choices=['executor', 'checker', 'generator'])
    tool_p.add_argument('--query')
    tool_p.add_argument('--limit', type=int, default=30)

    # Show single command/tool
    show_cmd_p = subparsers.add_parser('show-command', help='show details of one command')
    show_cmd_p.add_argument('name')

    show_tool_p = subparsers.add_parser('show-tool', help='show details of one tool')
    show_tool_p.add_argument('name')

    # Execute command/tool
    exec_cmd_p = subparsers.add_parser('exec-command', help='execute an economics command')
    exec_cmd_p.add_argument('name')
    exec_cmd_p.add_argument('prompt')

    exec_tool_p = subparsers.add_parser('exec-tool', help='execute an economics tool')
    exec_tool_p.add_argument('name')
    exec_tool_p.add_argument('payload')

    # Templates
    tmpl_list_p = subparsers.add_parser('templates', help='list code templates')
    tmpl_list_p.add_argument('--lang', choices=['stata', 'r', 'python'])

    tmpl_show_p = subparsers.add_parser('template', help='show a specific code template')
    tmpl_show_p.add_argument('name')
    tmpl_show_p.add_argument('--lang', choices=['stata', 'r', 'python'])

    # Context
    ctx_p = subparsers.add_parser('context', help='detect research project structure')
    ctx_p.add_argument('--path')

    # Session management
    bootstrap_p = subparsers.add_parser('bootstrap', help='start a new research session')
    bootstrap_p.add_argument('prompt')
    bootstrap_p.add_argument('--project', default='')
    bootstrap_p.add_argument('--limit', type=int, default=5)

    loop_p = subparsers.add_parser('turn-loop', help='run a multi-turn research session')
    loop_p.add_argument('prompt')
    loop_p.add_argument('--max-turns', type=int, default=3)

    subparsers.add_parser('sessions', help='list saved sessions')

    load_p = subparsers.add_parser('load-session', help='load a saved session')
    load_p.add_argument('session_id')

    # Integrity check
    integrity_p = subparsers.add_parser('integrity', help='check text for academic integrity issues')
    integrity_p.add_argument('text')

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == 'pipeline':
        print(render_pipeline())

    elif args.command == 'stage':
        stage = detect_stage(args.prompt)
        print(f'Detected stage: {stage}')

    elif args.command == 'route':
        runtime = EconRuntime()
        print(runtime.route_and_execute(args.prompt, args.limit))

    elif args.command == 'commands':
        print(render_command_index(limit=args.limit, query=args.query, stage=args.stage))

    elif args.command == 'tools':
        print(render_tool_index(limit=args.limit, query=args.query, kind=args.kind))

    elif args.command == 'show-command':
        cmd = get_command(args.name)
        if cmd:
            print(f'Name: {cmd.name}')
            print(f'Stage: {cmd.stage}')
            print(f'Responsibility: {cmd.responsibility}')
            print(f'Skill: {cmd.source_skill}')
            if cmd.template_hint:
                print(f'Template: {cmd.template_hint}')
        else:
            print(f'Command not found: {args.name}')
            return 1

    elif args.command == 'show-tool':
        tool = get_tool(args.name)
        if tool:
            print(f'Name: {tool.name}')
            print(f'Kind: {tool.kind}')
            print(f'Responsibility: {tool.responsibility}')
        else:
            print(f'Tool not found: {args.name}')
            return 1

    elif args.command == 'exec-command':
        result = execute_command(args.name, args.prompt)
        print(result.message)

    elif args.command == 'exec-tool':
        result = execute_tool(args.name, args.payload)
        print(result.message)

    elif args.command == 'templates':
        print(render_template_index(lang=args.lang))

    elif args.command == 'template':
        content = get_template(args.name, lang=args.lang)
        if content:
            print(content)
        else:
            print(f'Template not found: {args.name}')
            return 1

    elif args.command == 'context':
        base = Path(args.path) if args.path else None
        ctx = build_research_context(base)
        print(render_context(ctx))

    elif args.command == 'bootstrap':
        runtime = EconRuntime()
        matches = runtime.route_prompt(args.prompt, args.limit)
        engine = EconQueryEngine(project_name=args.project)
        matched_cmds = tuple(m.name for m in matches if m.kind == 'command')
        matched_tools = tuple(m.name for m in matches if m.kind == 'tool')
        result = engine.submit_message(args.prompt, matched_cmds, matched_tools)
        print(result.output)

        session = StoredSession(
            session_id=engine.session_id,
            project_name=engine.project_name,
            current_stage=detect_stage(args.prompt),
            messages=tuple(engine.mutable_messages),
            responses=(result.output,),
            input_tokens=engine.total_usage.input_tokens,
            output_tokens=engine.total_usage.output_tokens,
        )
        path = save_session(session)
        md_path = path.with_suffix('.md')
        md_path.write_text(
            f'# {args.project or "Research Session"}\n\n'
            f'**Prompt:** {args.prompt}\n\n'
            f'**Stage:** {session.current_stage} | '
            f'**Tokens:** {session.input_tokens} in / {session.output_tokens} out\n\n'
            f'---\n\n{result.output}\n',
            encoding='utf-8',
        )
        print(f'\n---\nSession saved: {path}')
        print(f'Markdown report: {md_path}')

    elif args.command == 'turn-loop':
        engine = EconQueryEngine(
            config=EconEngineConfig(max_turns=args.max_turns),
        )
        runtime = EconRuntime()

        prompts = [args.prompt]
        all_responses: list[str] = []
        for prompt in prompts:
            matches = runtime.route_prompt(prompt)
            matched_cmds = tuple(m.name for m in matches if m.kind == 'command')
            matched_tools = tuple(m.name for m in matches if m.kind == 'tool')
            result = engine.submit_message(prompt, matched_cmds, matched_tools)
            all_responses.append(result.output)
            print(result.output)
            print('---')

        session = StoredSession(
            session_id=engine.session_id,
            project_name=engine.project_name,
            current_stage=detect_stage(args.prompt),
            messages=tuple(engine.mutable_messages),
            responses=tuple(all_responses),
            input_tokens=engine.total_usage.input_tokens,
            output_tokens=engine.total_usage.output_tokens,
        )
        path = save_session(session)
        md_path = path.with_suffix('.md')
        md_content = '# Research Session\n\n'
        for i, (msg, resp) in enumerate(zip(session.messages, session.responses), 1):
            md_content += f'## Turn {i}\n\n**Prompt:** {msg}\n\n{resp}\n\n---\n\n'
        md_path.write_text(md_content, encoding='utf-8')
        print(f'\nSession saved: {path}')
        print(f'Markdown report: {md_path}')

    elif args.command == 'sessions':
        sessions = list_sessions()
        if sessions:
            for sid in sessions:
                print(sid)
        else:
            print('No saved sessions.')

    elif args.command == 'load-session':
        try:
            session = load_session(args.session_id)
            print(f'Session: {session.session_id}')
            print(f'Project: {session.project_name or "(unnamed)"}')
            print(f'Stage: {session.current_stage}')
            print(f'Turns: {len(session.messages)}')
            print(f'Tokens: {session.input_tokens} in / {session.output_tokens} out')
            print()
            for i, msg in enumerate(session.messages):
                print(f'--- Turn {i + 1} ---')
                print(f'Prompt: {msg}')
                if i < len(session.responses):
                    print()
                    print(session.responses[i])
                print()
            md_path = Path('.econ_sessions') / f'{args.session_id}.md'
            if md_path.exists():
                print(f'Full report: {md_path.resolve()}')
        except FileNotFoundError:
            print(f'Session not found: {args.session_id}')
            return 1

    elif args.command == 'integrity':
        warnings = check_integrity(args.text)
        print(render_integrity_report(warnings))

    return 0


if __name__ == '__main__':
    sys.exit(main())
