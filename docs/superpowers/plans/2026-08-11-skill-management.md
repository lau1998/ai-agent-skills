# AI Agent Skills Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化一个只包含开发类和其他类的 AI Agent Skills 仓库，并提供可重复使用的 `create-skill` Skill 完成分类、登记和校验。

**Architecture:** `skills/development` 与 `skills/other` 是唯一分类目录，根目录 `catalog.yaml` 保存统一索引。`create-skill` 负责智能判断分类，确定性登记由 Python 脚本完成；脚本使用 PyYAML 解析索引、校验重复项与路径，并通过临时文件原子更新。

**Tech Stack:** Markdown、YAML、Python 3.9+、PyYAML 6.x、`unittest`

## Global Constraints

- 分类值只能是 `development` 或 `other`。
- 分类依据是主要交付物；核心产物为代码或工程配置时使用 `development`，其余使用 `other`。
- Skill 名称只能包含小写字母、数字和连字符，且不超过 64 个字符。
- 不覆盖已有 Skill，不重复登记名称或路径。
- 所有函数使用文档注释，关键逻辑使用简短注释。
- 首版不增加子分类、标签、Web 界面或全局安装同步。

---

## File Map

- `AGENTS.md`：规定仓库内新增或更新 Skill 时必须使用本地 `create-skill`，并保存代码注释要求。
- `README.md`：说明目录、分类规则、环境准备和常用命令。
- `.gitignore`：忽略本地虚拟环境和 Python 缓存。
- `requirements-dev.txt`：固定 PyYAML 主版本范围。
- `catalog.yaml`：保存全部 Skill 的名称、分类、路径和简介。
- `skills/development/create-skill/SKILL.md`：定义创建、分类、初始化、登记和验证工作流。
- `skills/development/create-skill/agents/openai.yaml`：提供 Skill UI 元数据和默认调用提示。
- `skills/development/create-skill/scripts/register_skill.py`：确定性校验并原子更新目录索引。
- `tests/test_register_skill.py`：覆盖登记成功和所有拒绝场景。

### Task 1: Project Rules And Catalog Foundation

**Files:**
- Create: `.gitignore`
- Create: `requirements-dev.txt`
- Create: `AGENTS.md`
- Create: `README.md`
- Create: `catalog.yaml`
- Create: `skills/other/.gitkeep`

**Interfaces:**
- Produces: `catalog.yaml`，其根结构为 `{"version": 1, "skills": list[dict]}`。
- Produces: 唯一合法分类集合 `development`、`other`。

- [ ] **Step 1: Create the project foundation**

写入以下约定：

```yaml
# catalog.yaml
version: 1
skills: []
```

```text
# requirements-dev.txt
PyYAML>=6.0,<7.0
```

`AGENTS.md` 要求新增或更新 Skill 时读取 `skills/development/create-skill/SKILL.md`，并保留用户指定的关键代码注释和函数文档注释规则。`README.md` 记录两类判断规则以及 `.venv/bin/python -m unittest discover -s tests -v`、官方 `quick_validate.py` 的运行方式。

- [ ] **Step 2: Prepare the Python environment**

Run:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -c "import yaml; print(yaml.__version__)"
```

Expected: 最后一条命令输出 `6.x` 版本号。

- [ ] **Step 3: Verify the static structure**

Run: `find . -maxdepth 4 -type f -not -path './.git/*' | sort`

Expected: 输出包含根目录配置、`skills/other/.gitkeep` 和现有设计/计划文档。

- [ ] **Step 4: Commit**

```bash
git add .gitignore requirements-dev.txt AGENTS.md README.md catalog.yaml skills/other/.gitkeep
git commit -m "chore(skills): 初始化 Skill 管理目录"
```

### Task 2: Catalog Registration Script

**Files:**
- Create: `tests/test_register_skill.py`
- Create: `skills/development/create-skill/scripts/register_skill.py`

**Interfaces:**
- Produces: `register_skill(catalog_path: Path, root: Path, entry: dict[str, str]) -> None`。
- Produces: 命令行参数 `--catalog`、`--root`、`--name`、`--category`、`--path`、`--description`。
- Raises: `CatalogError`，用于非法目录结构、非法字段、重复名称、重复路径和不存在的 Skill 路径。

- [ ] **Step 1: Initialize the Skill scaffold with the official generator**

Run:

```bash
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/init_skill.py create-skill \
  --path skills/development \
  --resources scripts \
  --interface 'display_name=Create Skill' \
  --interface 'short_description=创建、分类并登记项目中的 AI Agent Skills' \
  --interface 'default_prompt=Use $create-skill to create and register a new AI Agent Skill in this repository.'
```

Expected: 创建 `skills/development/create-skill/SKILL.md`、`agents/openai.yaml` 和空的 `scripts/` 目录。

- [ ] **Step 2: Write failing registration tests**

测试用 `tempfile.TemporaryDirectory` 创建真实目录和目录文件，覆盖以下行为：

```python
def test_register_skill_appends_valid_entry(self):
    entry = {
        "name": "example-skill",
        "category": "development",
        "path": "skills/development/example-skill",
        "description": "Example development skill",
    }
    register_skill(self.catalog_path, self.root, entry)
    catalog = yaml.safe_load(self.catalog_path.read_text(encoding="utf-8"))
    self.assertEqual(catalog["skills"], [entry])

def test_register_skill_rejects_duplicate_name(self):
    register_skill(self.catalog_path, self.root, self.entry)
    duplicate = {**self.other_entry, "name": self.entry["name"]}
    with self.assertRaisesRegex(CatalogError, "name already registered"):
        register_skill(self.catalog_path, self.root, duplicate)

def test_register_skill_rejects_duplicate_path(self):
    register_skill(self.catalog_path, self.root, self.entry)
    duplicate = {**self.other_entry, "path": self.entry["path"]}
    with self.assertRaisesRegex(CatalogError, "path already registered"):
        register_skill(self.catalog_path, self.root, duplicate)

def test_register_skill_rejects_invalid_category(self):
    invalid = {**self.entry, "category": "business"}
    with self.assertRaisesRegex(CatalogError, "category must be"):
        register_skill(self.catalog_path, self.root, invalid)

def test_register_skill_rejects_missing_skill_directory(self):
    missing = {**self.entry, "path": "skills/development/missing"}
    with self.assertRaisesRegex(CatalogError, "skill directory does not exist"):
        register_skill(self.catalog_path, self.root, missing)
```

- [ ] **Step 3: Run tests and verify RED**

Run: `.venv/bin/python -m unittest tests.test_register_skill -v`

Expected: ERROR with `ModuleNotFoundError` for `register_skill` because the production script does not exist.

- [ ] **Step 4: Implement the minimal registration module**

实现以下公开结构，并为每个函数添加文档注释：

```python
ALLOWED_CATEGORIES = frozenset({"development", "other"})
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

class CatalogError(ValueError):
    """表示目录索引或待登记 Skill 不符合项目约束。"""

def load_catalog(catalog_path: Path) -> dict[str, Any]:
    """读取并验证目录索引的根结构。"""

def validate_entry(root: Path, entry: dict[str, str]) -> None:
    """验证单个 Skill 记录的字段、分类、名称和本地路径。"""

def register_skill(catalog_path: Path, root: Path, entry: dict[str, str]) -> None:
    """校验新记录并通过原子替换写回目录索引。"""

def build_parser() -> argparse.ArgumentParser:
    """创建登记命令的参数解析器。"""

def main(argv: Sequence[str] | None = None) -> int:
    """执行命令行登记流程并返回进程退出码。"""
```

写入时在 `catalog.yaml` 同目录创建临时文件，调用 `os.replace()` 原子替换。捕获 `CatalogError` 后通过参数解析器输出错误并返回非零退出状态，不输出 Python traceback。

- [ ] **Step 5: Run tests and verify GREEN**

Run: `.venv/bin/python -m unittest tests.test_register_skill -v`

Expected: 5 tests PASS。

- [ ] **Step 6: Add CLI coverage**

增加一项测试，调用 `main([...])` 登记真实 Skill 目录并断言返回 `0`；同时捕获标准输出并断言包含 `Registered example-skill as development`。

- [ ] **Step 7: Run all tests**

Run: `.venv/bin/python -m unittest discover -s tests -v`

Expected: 6 tests PASS，无 warning 和 traceback。

- [ ] **Step 8: Commit**

```bash
git add tests/test_register_skill.py skills/development/create-skill/scripts/register_skill.py
git commit -m "feat(catalog): 增加 Skill 原子登记脚本"
```

### Task 3: Create-Skill Workflow

**Files:**
- Modify: `skills/development/create-skill/SKILL.md`
- Modify: `skills/development/create-skill/agents/openai.yaml`
- Modify: `catalog.yaml`

**Interfaces:**
- Consumes: `register_skill.py` 的命令行参数。
- Produces: `$create-skill` Skill，触发新增、创建、分类或更新本仓库 Skill 的请求。

- [ ] **Step 1: Replace generated placeholders with the approved workflow**

`SKILL.md` frontmatter 只保留：

```yaml
---
name: create-skill
description: Create, classify, register, or update AI Agent Skills in this repository. Use when the user asks to add, create, scaffold, organize, categorize, validate, or modify a Skill managed by this project.
---
```

正文必须要求：先读取根目录 `AGENTS.md` 和 `catalog.yaml`；先用具体示例确认需求；使用官方 `skill-creator` 初始化流程；按主要交付物自动选择 `development` 或 `other`；说明分类结果；仅在实质歧义时询问；不覆盖现有目录；校验成功后调用登记脚本；更新已有 Skill 时保持原路径和索引唯一性。

- [ ] **Step 2: Register create-skill**

Run:

```bash
.venv/bin/python skills/development/create-skill/scripts/register_skill.py \
  --catalog catalog.yaml \
  --root . \
  --name create-skill \
  --category development \
  --path skills/development/create-skill \
  --description '创建、分类、登记并校验项目中的 AI Agent Skills'
```

Expected: `Registered create-skill as development`，且 `catalog.yaml` 只有一条记录。

- [ ] **Step 3: Validate the Skill**

Run:

```bash
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/development/create-skill
```

Expected: `Skill is valid!`

- [ ] **Step 4: Commit**

```bash
git add catalog.yaml skills/development/create-skill
git commit -m "feat(skills): 增加 Skill 创建与自动分类流程"
```

### Task 4: End-To-End Verification

**Files:**
- Modify: `README.md` only if verification exposes an incorrect command.

**Interfaces:**
- Consumes: 完整仓库结构、测试命令、官方 Skill 校验器。
- Produces: 可重复执行的项目验证结果。

- [ ] **Step 1: Run unit tests**

Run: `.venv/bin/python -m unittest discover -s tests -v`

Expected: 6 tests PASS。

- [ ] **Step 2: Run Skill validation**

Run: `.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/development/create-skill`

Expected: `Skill is valid!`

- [ ] **Step 3: Check repository integrity**

Run:

```bash
.venv/bin/python -c "from pathlib import Path; import yaml; data=yaml.safe_load(Path('catalog.yaml').read_text()); assert data['version'] == 1; assert {item['category'] for item in data['skills']} <= {'development', 'other'}; assert all(Path(item['path']).is_dir() for item in data['skills']); assert len({item['name'] for item in data['skills']}) == len(data['skills']); assert len({item['path'] for item in data['skills']}) == len(data['skills']); print('catalog integrity: ok')"
```

Expected: `catalog integrity: ok`。

- [ ] **Step 4: Check formatting and worktree state**

Run: `git diff --check && git status --short`

Expected: 无空白错误；只显示本次尚未提交的计划状态或为空。

- [ ] **Step 5: Commit verification documentation fixes if any**

如果 README 命令无需修正，不创建空提交。如果发生修正：

```bash
git add README.md
git commit -m "docs(skills): 修正项目验证命令"
```
