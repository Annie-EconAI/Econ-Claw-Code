<div align="center">

# Econ-Claw-Code

**From research question to submission — one CLI for the entire empirical workflow.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests: 46 passing](https://img.shields.io/badge/tests-46%20passing-brightgreen.svg)](tests/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)]()

[English](README.md) | [中文](README_CN.md)

</div>

---

Empirical research involves a lot of repeated work — choosing the right estimator, setting up regression boilerplate, checking results before submission. Most of it isn't hard, but it takes time and it's easy to miss things.

**Econ-Claw-Code** is a lightweight CLI that streamlines this workflow. Describe your research task in plain language, and it matches you to the right econometric method, provides ready-to-use code templates in Stata, R, or Python, and flags common issues — like leftover placeholders or mismatched numbers — before the referee does.

```bash
$ econ-claw route "estimate the effect of minimum wage on employment using DiD"

Detected stage: analysis
Matches:
  - [command] did          (stage=analysis, score=5)
  - [command] regress      (stage=analysis, score=4)
  - [command] event-study  (stage=analysis, score=4)
```

**Zero dependencies.** Pure Python 3.10+. Runs immediately.

---

## Why This Tool?

| Pain point | How Econ-Claw-Code helps |
|------------|---------------------------|
| "Which estimator do I need for staggered treatment?" | Describe your research in plain English → get matched to the right method |
| "Where's my reghdfe template from last year?" | 11 publication-ready templates (Stata/R/Python) — always one command away |
| "Did I check parallel trends?" | 23 built-in checkers catch missing pre-trends, weak instruments, clustering errors |
| "The referee says my number on p.12 doesn't match Table 3" | `verify-numbers` cross-checks hardcoded LaTeX values against code output |
| "Is this draft ready to submit?" | `integrity` catches placeholders (XXX/TODO), causal overstatement, citation gaps |

---

## Who Is This For?

- **Undergraduates** working on empirical term papers or honors theses
- **Master's / PhD students** writing dissertations or job market papers
- **Research assistants** running regressions and building replication packages
- **Faculty and postdocs** juggling multiple empirical projects
- **Policy researchers** in think tanks, government agencies, and international organizations

Whether you study economics, political science, sociology, public health, or any field that uses causal inference with observational data — if you use Stata, R, or Python for empirical research, this tool is for you.

---

## Quick Start

```bash
git clone https://github.com/Annie-EconAI/Econ-Claw-Code.git
cd Econ-Claw-Code

# Run directly (no install needed)
python -m src.main pipeline

# Or install as a global CLI tool
pip install -e .
econ-claw pipeline
```

---

## What's Inside

### 1. Research Pipeline — 6 Stages

```bash
econ-claw pipeline
```

```
DATA       → Cleaning, merging, descriptive statistics, balance tables
ANALYSIS   → Regressions, causal inference, identification strategies
VIZ        → Publication-ready figures, plots, and charts
WRITE      → Abstract, introduction, model, data section, results, conclusion
REVIEW     → Referee reports, self-review, R&R response, magnitude assessment
SUBMIT     → Compilation check, number verification, citation audit, formatting
```

### 2. Smart Routing — Describe What You Need

The core feature. Give it natural language, get back the right tools:

```bash
econ-claw route "test for parallel trends before running DiD"
# → parallel-trends, did, event-study, pretrend-checker

econ-claw route "write a referee report"
# → referee-report, self-review, rr-response

econ-claw stage "check if my IV first stage is strong enough"
# → Detected stage: submit
```

The router detects your research stage automatically and boosts commands from that stage.

### 3. 37 Economics Commands

Every major method in applied micro, organized by pipeline stage:

```bash
econ-claw commands                     # list all 37
econ-claw commands --stage analysis    # filter by stage
econ-claw commands --query "event"     # search
econ-claw show-command event-study     # view details
```

**Highlights by stage:**

| Stage | Key Commands |
|-------|-------------|
| **DATA** | `balance-table`, `summary-stats`, `clean-data`, `merge-data` |
| **ANALYSIS** | `regress`, `did`, `staggered-did`, `event-study`, `iv-2sls`, `rdd`, `synth-control`, `bunching`, `shift-share` |
| **VIZ** | `coefficient-plot`, `event-study-plot`, `binscatter`, `rdd-plot`, `parallel-trends` |
| **WRITE** | `write-abstract`, `write-intro`, `write-results`, `write-conclusion` |
| **REVIEW** | `referee-report`, `self-review`, `rr-response`, `magnitude-check` |
| **SUBMIT** | `pre-submit-check`, `verify-numbers`, `check-citations`, `check-compilation` |

<details>
<summary>📋 Full command list (37 commands)</summary>

**DATA** (5): `describe-data`, `clean-data`, `merge-data`, `balance-table`, `summary-stats`

**ANALYSIS** (10): `regress`, `iv-2sls`, `did`, `staggered-did`, `event-study`, `rdd`, `synth-control`, `bunching`, `shift-share`, `mht-correction`

**VIZ** (6): `coefficient-plot`, `event-study-plot`, `binscatter`, `rdd-plot`, `parallel-trends`, `forest-plot`

**WRITE** (7): `write-abstract`, `write-intro`, `write-model`, `write-data-section`, `write-results`, `write-conclusion`, `write-title`

**REVIEW** (4): `referee-report`, `self-review`, `rr-response`, `magnitude-check`

**SUBMIT** (4): `pre-submit-check`, `verify-numbers`, `check-citations`, `check-compilation`

</details>

### 4. 23 Research Tools

```bash
econ-claw tools                     # list all 23
econ-claw tools --kind checker      # executors, checkers, or generators
```

| Category | Tools |
|----------|-------|
| **Executors** (4) | `stata-runner`, `r-runner`, `python-runner`, `latex-compiler` |
| **Checkers** (9) | `number-verifier`, `citation-checker`, `integrity-guard`, `mht-checker`, `compilation-checker`, `clustering-checker`, `pretrend-checker`, `first-stage-checker`, `placeholder-scanner` |
| **Generators** (10) | `table-generator`, `figure-generator`, `bib-manager`, `template-engine`, `replication-packager`, `balance-table-gen`, `summary-stats-gen`, `dofile-header-gen`, `referee-report-gen`, `rr-response-gen` |

### 5. 11 Code Templates — Copy and Use

Publication-ready templates you can paste directly into your project:

```bash
econ-claw templates                 # list all 11
econ-claw templates --lang stata    # filter by language
econ-claw template event-study      # output a template
```

| Language | Templates |
|----------|-----------|
| **Stata** (6) | `reghdfe-main`, `event-study`, `balance-table`, `summary-stats`, `did`, `dofile-header` |
| **R** (3) | `fixest-main`, `honest-did` (Rambachan & Roth 2023), `cs-did` (Callaway & Sant'Anna) |
| **Python** (2) | `romano-wolf` (MHT correction), `panel-reg` (linearmodels) |

**Example** — get an event study template:

```bash
$ econ-claw template event-study --lang stata
```

```stata
* Event Study Estimation with Leads and Lags
* Requires: reghdfe, coefplot

forvalues k = ${LEADS_MAX}(-1)1 {
    gen lead`k' = (event_time == -`k')
}
forvalues k = 0/${LAGS_MAX} {
    gen lag`k' = (event_time == `k')
}
drop lead1

reghdfe ${DEPVAR} lead* lag*, absorb(${FE1} ${FE2}) cluster(${CLUSTER})
coefplot, keep(lead* lag*) vertical yline(0) ...
```

### 6. Session Management

Track your research progress across sessions:

```bash
econ-claw bootstrap "estimate treatment effect using IV" --project my-paper
econ-claw turn-loop "run the main regression" --max-turns 5
econ-claw sessions              # list saved sessions
econ-claw load-session <id>     # reload a past session
```

Sessions are saved to `.econ_sessions/` as JSON + Markdown reports.

### 7. Project Context Detection

Auto-detect your research project structure:

```bash
econ-claw context --path /path/to/my-paper
```

```
Root: /path/to/my-paper
Data: data/    Code: code/    Output: output/    Paper: paper/
Stata: 12 files | R: 3 files | Python: 5 files | LaTeX: 2 files
```

### 8. Academic Integrity Check

Catch common problems before submission:

```bash
$ econ-claw integrity "This proves that X caused Y and the coefficient is XXX"

# Integrity Check (2 issues)
[ERROR] [fabrication] Unresolved placeholder found
[WARN]  [causality] Causal language — ensure identification strategy supports this
```

What it catches:
- **Placeholders**: XXX, TODO, ???
- **Causal overstatement**: "proves", "caused by" without identification support
- **Citation gaps**: year references without `\cite`

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `pipeline` | Show 6-stage research pipeline |
| `stage <prompt>` | Detect pipeline stage |
| `route <prompt>` | Route to matching commands/tools |
| `commands` | List commands (`--stage`, `--query`, `--limit`) |
| `tools` | List tools (`--kind`, `--query`, `--limit`) |
| `show-command <name>` | Command details |
| `show-tool <name>` | Tool details |
| `exec-command <name> <prompt>` | Execute command |
| `exec-tool <name> <payload>` | Execute tool |
| `templates` | List code templates (`--lang`) |
| `template <name>` | Show template content (`--lang`) |
| `context` | Detect project structure (`--path`) |
| `bootstrap <prompt>` | Start session (`--project`, `--limit`) |
| `turn-loop <prompt>` | Multi-turn session (`--max-turns`) |
| `sessions` | List saved sessions |
| `load-session <id>` | Load session |
| `integrity <text>` | Integrity check |

---

## Architecture

```
src/
├── main.py              # CLI entrypoint (17 subcommands)
├── models.py            # 12 frozen dataclasses
├── commands.py          # 37 economics commands (JSON + LRU cache)
├── tools.py             # 23 research tools (JSON + LRU cache)
├── pipeline.py          # 6-stage pipeline + keyword detection
├── runtime.py           # Prompt router with stage-aware scoring
├── query_engine.py      # Multi-turn session engine
├── context.py           # Project directory detection
├── session_store.py     # Session persistence (JSON + Markdown)
├── templates.py         # Code template registry
├── integrity.py         # Academic integrity checker
└── reference_data/
    ├── commands_snapshot.json
    ├── tools_snapshot.json
    ├── pipeline_stages.json
    └── templates/
        ├── stata/       # reghdfe, event study, balance table, ...
        ├── r/           # fixest, HonestDiD, Callaway-Sant'Anna
        └── python/      # Romano-Wolf, panel regression
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We welcome:
- New econometric command definitions
- Code templates for additional methods
- Bug reports and feature requests

## Tests

```bash
python -m pytest tests/ -v
# 46 tests, all passing
```

## Requirements

- Python 3.10+
- No external dependencies (stdlib only)

## License

MIT
