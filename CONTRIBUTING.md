# Contributing to Econ-Claw-Code

Thank you for your interest in contributing! This project aims to help economists and social scientists with their empirical research workflow.

## How to Contribute

### Reporting Bugs

Open an issue with:
- What you expected to happen
- What actually happened
- Steps to reproduce
- Your Python version (`python --version`)

### Suggesting Features

Open an issue describing:
- The research task you're trying to accomplish
- How the tool could help
- Which pipeline stage it belongs to (data/analysis/viz/write/review/submit)

### Adding a New Command

Commands are defined in `src/reference_data/commands_snapshot.json`. Each entry needs:

```json
{
  "name": "your-command-name",
  "stage": "analysis",
  "responsibility": "Short description of what this command does",
  "source_skill": "econ-coding-viz",
  "template_hint": "stata/your_template.do"
}
```

### Adding a Code Template

1. Create the template file in `src/reference_data/templates/{stata,r,python}/`
2. Use `${VARIABLE}` placeholders for user-specific values
3. Register it in `src/templates.py`

### Adding a New Tool

Tools are defined in `src/reference_data/tools_snapshot.json`. Each entry needs:

```json
{
  "name": "your-tool-name",
  "kind": "checker",
  "responsibility": "Short description of what this tool does"
}
```

## Development Setup

```bash
git clone https://github.com/Annie-EconAI/Econ-Claw-Code.git
cd Econ-Claw-Code
python -m pytest tests/ -v    # run tests
```

No dependencies to install — the project uses only the Python standard library.

## Code Style

- Pure Python 3.10+, no external dependencies
- Frozen dataclasses for data models
- Type hints throughout
- Keep it simple — this tool should be easy to understand and modify

## Running Tests

```bash
python -m pytest tests/ -v
```

All 46 tests should pass before submitting a PR.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
