"""Tests for econ-claw-code."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

# Ensure src is importable
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.models import EconCommand, EconTool, UsageSummary, StoredSession
from src.commands import ECON_COMMANDS, get_command, find_commands, execute_command, get_commands
from src.tools import ECON_TOOLS, get_tool, find_tools, execute_tool, get_tools
from src.pipeline import PIPELINE_STAGES, detect_stage, STAGE_ORDER
from src.runtime import EconRuntime
from src.query_engine import EconQueryEngine, EconEngineConfig
from src.context import build_research_context
from src.session_store import save_session, load_session
from src.templates import list_templates, get_template
from src.integrity import check_integrity
from src.main import main as cli_main


class TestModels(unittest.TestCase):
    def test_econ_command_frozen(self):
        cmd = EconCommand('test', 'data', 'test cmd', 'skill', '')
        with self.assertRaises(AttributeError):
            cmd.name = 'other'  # type: ignore

    def test_usage_summary_add(self):
        u = UsageSummary(10, 20)
        u2 = u.add_turn(5, 10)
        self.assertEqual(u2.input_tokens, 15)
        self.assertEqual(u2.output_tokens, 30)


class TestCommands(unittest.TestCase):
    def test_snapshot_loaded(self):
        self.assertGreater(len(ECON_COMMANDS), 20)

    def test_get_command(self):
        cmd = get_command('regress')
        self.assertIsNotNone(cmd)
        self.assertEqual(cmd.stage, 'analysis')

    def test_get_command_missing(self):
        self.assertIsNone(get_command('nonexistent'))

    def test_find_commands(self):
        results = find_commands('regression fixed effects')
        self.assertGreater(len(results), 0)
        names = [c.name for c in results]
        self.assertIn('regress', names)

    def test_get_commands_by_stage(self):
        analysis_cmds = get_commands('analysis')
        self.assertTrue(all(c.stage == 'analysis' for c in analysis_cmds))
        self.assertGreater(len(analysis_cmds), 5)

    def test_execute_command(self):
        result = execute_command('regress', 'run a regression')
        self.assertIn('regress', result.message)

    def test_execute_unknown(self):
        result = execute_command('fake', 'test')
        self.assertIn('Unknown', result.message)


class TestTools(unittest.TestCase):
    def test_snapshot_loaded(self):
        self.assertGreater(len(ECON_TOOLS), 15)

    def test_get_tool(self):
        tool = get_tool('stata-runner')
        self.assertIsNotNone(tool)
        self.assertEqual(tool.kind, 'executor')

    def test_get_tools_by_kind(self):
        checkers = get_tools('checker')
        self.assertTrue(all(t.kind == 'checker' for t in checkers))

    def test_find_tools(self):
        results = find_tools('verify number')
        self.assertGreater(len(results), 0)


class TestPipeline(unittest.TestCase):
    def test_stages_loaded(self):
        self.assertEqual(len(PIPELINE_STAGES), 6)

    def test_stage_order(self):
        self.assertEqual(STAGE_ORDER, ('data', 'analysis', 'viz', 'write', 'review', 'submit'))

    def test_detect_stage_analysis(self):
        stage = detect_stage('run a regression with fixed effects')
        self.assertEqual(stage, 'analysis')

    def test_detect_stage_write(self):
        stage = detect_stage('write the introduction paragraph')
        self.assertEqual(stage, 'write')

    def test_detect_stage_submit(self):
        stage = detect_stage('check latex compilation and verify citations')
        self.assertEqual(stage, 'submit')

    def test_detect_stage_data(self):
        stage = detect_stage('clean the data and handle missing values')
        self.assertEqual(stage, 'data')

    def test_detect_stage_viz(self):
        stage = detect_stage('plot a coefficient plot with confidence intervals')
        self.assertEqual(stage, 'viz')

    def test_detect_stage_review(self):
        stage = detect_stage('generate a referee report and assess identification threats')
        self.assertEqual(stage, 'review')


class TestRuntime(unittest.TestCase):
    def test_route_prompt(self):
        runtime = EconRuntime()
        matches = runtime.route_prompt('run a regression with fixed effects')
        self.assertGreater(len(matches), 0)
        # regress command should be among top matches
        names = [m.name for m in matches]
        self.assertIn('regress', names)

    def test_route_and_execute(self):
        runtime = EconRuntime()
        report = runtime.route_and_execute('estimate event study')
        self.assertIn('Routing Report', report)
        self.assertIn('event-study', report)

    def test_stage_boost(self):
        runtime = EconRuntime()
        matches = runtime.route_prompt('write the abstract for this paper', limit=10)
        # write-abstract should be boosted due to stage detection
        top_names = [m.name for m in matches[:3]]
        self.assertIn('write-abstract', top_names)


class TestQueryEngine(unittest.TestCase):
    def test_submit_message(self):
        engine = EconQueryEngine()
        result = engine.submit_message('test prompt', ('regress',), ('stata-runner',))
        self.assertEqual(result.stop_reason, 'completed')
        self.assertIn('regress', result.output)

    def test_max_turns(self):
        engine = EconQueryEngine(config=EconEngineConfig(max_turns=2))
        engine.submit_message('turn 1')
        engine.submit_message('turn 2')
        result = engine.submit_message('turn 3')
        self.assertEqual(result.stop_reason, 'max_turns_reached')

    def test_render_summary(self):
        engine = EconQueryEngine(project_name='test-project')
        engine.submit_message('test')
        summary = engine.render_summary()
        self.assertIn('test-project', summary)

    def test_stream(self):
        engine = EconQueryEngine()
        events = list(engine.stream_submit_message('test', ('regress',)))
        types = [e['type'] for e in events]
        self.assertIn('message_start', types)
        self.assertIn('message_stop', types)


class TestSessionStore(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            session = StoredSession(
                session_id='test123',
                project_name='my-paper',
                current_stage='analysis',
                messages=('msg1', 'msg2'),
                input_tokens=100,
                output_tokens=200,
            )
            save_session(session, directory=tmpdir)
            loaded = load_session('test123', directory=tmpdir)
            self.assertEqual(loaded.session_id, 'test123')
            self.assertEqual(loaded.project_name, 'my-paper')
            self.assertEqual(len(loaded.messages), 2)


class TestTemplates(unittest.TestCase):
    def test_list_all(self):
        templates = list_templates()
        self.assertGreater(len(templates), 5)

    def test_list_stata(self):
        templates = list_templates('stata')
        self.assertTrue(all(t.lang == 'stata' for t in templates))

    def test_get_template(self):
        content = get_template('reghdfe-main', 'stata')
        self.assertIsNotNone(content)
        self.assertIn('reghdfe', content)


class TestIntegrity(unittest.TestCase):
    def test_clean_text(self):
        warnings = check_integrity('This is a normal sentence about economics.')
        self.assertEqual(len(warnings), 0)

    def test_placeholder_detected(self):
        warnings = check_integrity('The coefficient is XXX and we need to fill it in.')
        self.assertTrue(any(w.category == 'fabrication' for w in warnings))

    def test_causal_language(self):
        warnings = check_integrity('This proves that X caused Y.')
        self.assertTrue(any(w.category == 'causality' for w in warnings))


class TestCLI(unittest.TestCase):
    def test_pipeline(self):
        self.assertEqual(cli_main(['pipeline']), 0)

    def test_stage(self):
        self.assertEqual(cli_main(['stage', 'run a regression']), 0)

    def test_route(self):
        self.assertEqual(cli_main(['route', 'estimate did effect']), 0)

    def test_commands(self):
        self.assertEqual(cli_main(['commands']), 0)

    def test_commands_stage(self):
        self.assertEqual(cli_main(['commands', '--stage', 'analysis']), 0)

    def test_tools(self):
        self.assertEqual(cli_main(['tools']), 0)

    def test_templates(self):
        self.assertEqual(cli_main(['templates']), 0)

    def test_template_show(self):
        self.assertEqual(cli_main(['template', 'reghdfe-main']), 0)

    def test_show_command(self):
        self.assertEqual(cli_main(['show-command', 'regress']), 0)

    def test_show_tool(self):
        self.assertEqual(cli_main(['show-tool', 'stata-runner']), 0)

    def test_integrity(self):
        self.assertEqual(cli_main(['integrity', 'normal text']), 0)


if __name__ == '__main__':
    unittest.main()
