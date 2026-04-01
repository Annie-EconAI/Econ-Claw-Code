<div align="center">

# Econ-Claw-Code

**从研究问题到投稿——一个命令行工具覆盖整个实证研究流程。**

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Tests: 46 passing](https://img.shields.io/badge/tests-46%20passing-brightgreen.svg)](tests/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)]()

[English](README.md) | [中文](README_CN.md)

</div>

---

实证研究中有大量重复性工作——选择合适的估计方法、搭建回归代码框架、投稿前逐项检查。这些事情本身不难，但耗时间，也容易遗漏。

**Econ-Claw-Code** 是一个轻量级命令行工具，用来简化这些流程。用自然语言描述你的研究任务，它会匹配正确的计量方法，提供 Stata、R 或 Python 的现成代码模板，并在审稿人之前帮你发现常见问题——比如残留的占位符或对不上的数字。

```bash
$ econ-claw route "estimate the effect of minimum wage on employment using DiD"

Detected stage: analysis
Matches:
  - [command] did          (stage=analysis, score=5)
  - [command] regress      (stage=analysis, score=4)
  - [command] event-study  (stage=analysis, score=4)
```

**零依赖。** 纯 Python 3.10+，开箱即用。

---

## 为什么需要这个工具？

| 痛点 | Econ-Claw-Code 怎么帮你 |
|------|--------------------------|
| "交错处理该用哪个估计量？" | 用自然语言描述研究需求 → 自动匹配正确方法 |
| "去年写的 reghdfe 模板放哪了？" | 11 个发表级代码模板（Stata/R/Python），一条命令调出 |
| "平行趋势检验了吗？" | 23 个内置检查器，覆盖平行趋势、弱工具变量、聚类错误等 |
| "审稿人说第 12 页的数字和表 3 对不上" | `verify-numbers` 自动交叉核验 LaTeX 中的硬编码数字 |
| "这稿子能投了吗？" | `integrity` 检测占位符（XXX/TODO）、因果过度表述、引文缺失 |

---

## 适用人群

- **本科生** —— 正在写实证课程论文或毕业论文
- **硕士生 / 博士生** —— 撰写学位论文或 Job Market Paper
- **研究助理（RA）** —— 跑回归、搭建 replication package
- **教职人员和博士后** —— 同时推进多个实证项目
- **政策研究者** —— 智库、政府机构、国际组织的研究人员

无论你研究经济学、政治学、社会学、公共卫生，还是其他使用观测数据做因果推断的领域——只要你用 Stata、R 或 Python 做实证研究，这个工具就是为你准备的。

---

## 快速开始

```bash
git clone https://github.com/Annie-EconAI/Econ-Claw-Code.git
cd Econ-Claw-Code

# 直接运行（无需安装）
python -m src.main pipeline

# 或者安装为全局命令行工具
pip install -e .
econ-claw pipeline
```

---

## 功能全览

### 1. 研究流水线 — 6 个阶段

```bash
econ-claw pipeline
```

```
DATA       → 数据清洗、合并、描述性统计、平衡性检验
ANALYSIS   → 回归分析、因果推断、识别策略
VIZ        → 发表级图表和可视化
WRITE      → 摘要、引言、模型、数据、结果、结论
REVIEW     → 审稿报告、自我审查、修改回复、效应量评估
SUBMIT     → 编译检查、数字核验、引文审查、格式规范
```

### 2. 智能路由 — 用自然语言描述你的需求

核心功能。输入自然语言，返回匹配的计量方法：

```bash
econ-claw route "test for parallel trends before running DiD"
# → parallel-trends, did, event-study, pretrend-checker

econ-claw route "write a referee report"
# → referee-report, self-review, rr-response

econ-claw stage "check if my IV first stage is strong enough"
# → Detected stage: submit
```

路由器自动检测你所处的研究阶段，并对该阶段的命令给予加分。

**路由原理：**

```
用户输入: "estimate DiD effect on employment"
  ↓
pipeline.py → detect_stage() → "analysis"        （关键词匹配）
  ↓
runtime.py → route_prompt() → 评分 + 阶段加分    （同阶段 +2 分）
  ↓
返回排名最高的匹配结果
```

### 3. 37 个经济学命令

覆盖应用微观的所有主流方法，按研究阶段组织：

```bash
econ-claw commands                     # 列出全部 37 个
econ-claw commands --stage analysis    # 按阶段筛选
econ-claw commands --query "event"     # 关键词搜索
econ-claw show-command event-study     # 查看详情
```

**各阶段亮点：**

| 阶段 | 核心命令 |
|------|----------|
| **DATA** | `balance-table`、`summary-stats`、`clean-data`、`merge-data` |
| **ANALYSIS** | `regress`、`did`、`staggered-did`、`event-study`、`iv-2sls`、`rdd`、`synth-control`、`bunching`、`shift-share` |
| **VIZ** | `coefficient-plot`、`event-study-plot`、`binscatter`、`rdd-plot`、`parallel-trends` |
| **WRITE** | `write-abstract`、`write-intro`、`write-results`、`write-conclusion` |
| **REVIEW** | `referee-report`、`self-review`、`rr-response`、`magnitude-check` |
| **SUBMIT** | `pre-submit-check`、`verify-numbers`、`check-citations`、`check-compilation` |

<details>
<summary>📋 完整命令清单（37 个）</summary>

**DATA**（5 个）：`describe-data`、`clean-data`、`merge-data`、`balance-table`、`summary-stats`

**ANALYSIS**（10 个）：`regress`、`iv-2sls`、`did`、`staggered-did`、`event-study`、`rdd`、`synth-control`、`bunching`、`shift-share`、`mht-correction`

**VIZ**（6 个）：`coefficient-plot`、`event-study-plot`、`binscatter`、`rdd-plot`、`parallel-trends`、`forest-plot`

**WRITE**（7 个）：`write-abstract`、`write-intro`、`write-model`、`write-data-section`、`write-results`、`write-conclusion`、`write-title`

**REVIEW**（4 个）：`referee-report`、`self-review`、`rr-response`、`magnitude-check`

**SUBMIT**（4 个）：`pre-submit-check`、`verify-numbers`、`check-citations`、`check-compilation`

</details>

### 4. 23 个研究工具

```bash
econ-claw tools                     # 列出全部 23 个
econ-claw tools --kind checker      # 按类别筛选：executor / checker / generator
```

| 类别 | 工具 |
|------|------|
| **执行器**（4 个） | `stata-runner`、`r-runner`、`python-runner`、`latex-compiler` |
| **检查器**（9 个） | `number-verifier`、`citation-checker`、`integrity-guard`、`mht-checker`、`compilation-checker`、`clustering-checker`、`pretrend-checker`、`first-stage-checker`、`placeholder-scanner` |
| **生成器**（10 个） | `table-generator`、`figure-generator`、`bib-manager`、`template-engine`、`replication-packager`、`balance-table-gen`、`summary-stats-gen`、`dofile-header-gen`、`referee-report-gen`、`rr-response-gen` |

### 5. 11 个代码模板 — 复制即用

发表级代码模板，直接粘贴到你的项目中：

```bash
econ-claw templates                 # 列出全部 11 个
econ-claw templates --lang stata    # 按语言筛选
econ-claw template event-study      # 输出模板内容
```

| 语言 | 模板 |
|------|------|
| **Stata**（6 个） | `reghdfe-main`、`event-study`、`balance-table`、`summary-stats`、`did`、`dofile-header` |
| **R**（3 个） | `fixest-main`、`honest-did`（Rambachan & Roth 2023）、`cs-did`（Callaway & Sant'Anna） |
| **Python**（2 个） | `romano-wolf`（多重假设检验校正）、`panel-reg`（面板回归） |

**示例** — 获取 Event Study 模板：

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

### 6. 会话管理

跟踪研究进度，跨会话保存和恢复：

```bash
econ-claw bootstrap "estimate treatment effect using IV" --project my-paper
econ-claw turn-loop "run the main regression" --max-turns 5
econ-claw sessions              # 列出已保存的会话
econ-claw load-session <id>     # 恢复历史会话
```

会话保存在 `.econ_sessions/` 目录，格式为 JSON + Markdown 报告。

### 7. 项目上下文检测

自动识别研究项目结构：

```bash
econ-claw context --path /path/to/my-paper
```

```
Root: /path/to/my-paper
Data: data/    Code: code/    Output: output/    Paper: paper/
Stata: 12 files | R: 3 files | Python: 5 files | LaTeX: 2 files
```

### 8. 学术规范检查

投稿前扫描常见问题：

```bash
$ econ-claw integrity "This proves that X caused Y and the coefficient is XXX"

# Integrity Check (2 issues)
[ERROR] [fabrication] Unresolved placeholder found
[WARN]  [causality] Causal language — ensure identification strategy supports this
```

检查内容：
- **占位符** ：XXX、TODO、???
- **因果过度表述**："proves"、"caused by" 等缺乏识别策略支持的表述
- **引文缺失**：含年份引用但缺少 `\cite`

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `pipeline` | 显示 6 阶段研究流水线 |
| `stage <prompt>` | 检测研究阶段 |
| `route <prompt>` | 路由到匹配的命令/工具 |
| `commands` | 列出命令（`--stage`、`--query`、`--limit`） |
| `tools` | 列出工具（`--kind`、`--query`、`--limit`） |
| `show-command <name>` | 查看命令详情 |
| `show-tool <name>` | 查看工具详情 |
| `exec-command <name> <prompt>` | 执行命令 |
| `exec-tool <name> <payload>` | 执行工具 |
| `templates` | 列出代码模板（`--lang`） |
| `template <name>` | 显示模板内容（`--lang`） |
| `context` | 检测项目结构（`--path`） |
| `bootstrap <prompt>` | 启动会话（`--project`、`--limit`） |
| `turn-loop <prompt>` | 多轮会话（`--max-turns`） |
| `sessions` | 列出已保存的会话 |
| `load-session <id>` | 加载会话 |
| `integrity <text>` | 学术规范检查 |

---

## 项目架构

```
src/
├── main.py              # CLI 入口（17 个子命令）
├── models.py            # 12 个冻结数据类
├── commands.py          # 37 个经济学命令（JSON + LRU 缓存）
├── tools.py             # 23 个研究工具（JSON + LRU 缓存）
├── pipeline.py          # 6 阶段流水线 + 关键词检测
├── runtime.py           # 提示词路由器 + 阶段感知评分
├── query_engine.py      # 多轮会话引擎
├── context.py           # 项目目录检测
├── session_store.py     # 会话持久化（JSON + Markdown）
├── templates.py         # 代码模板注册表
├── integrity.py         # 学术规范检查器
└── reference_data/
    ├── commands_snapshot.json
    ├── tools_snapshot.json
    ├── pipeline_stages.json
    └── templates/
        ├── stata/       # reghdfe、事件研究、平衡表……
        ├── r/           # fixest、HonestDiD、Callaway-Sant'Anna
        └── python/      # Romano-Wolf、面板回归
```

---

## 参与贡献

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。我们欢迎：
- 新增计量方法命令定义
- 新增代码模板
- Bug 报告和功能建议

## 测试

```bash
python -m pytest tests/ -v
# 46 个测试，全部通过
```

## 环境要求

- Python 3.10+
- 无外部依赖（仅使用标准库）

## 许可证

MIT
