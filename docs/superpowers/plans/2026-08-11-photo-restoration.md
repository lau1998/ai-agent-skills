# Photo Restoration Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `other` 分类下创建并登记一个基于 ImageGen 的 `photo-restoration` Skill，默认忠实修复老照片，按需提供现代增强。

**Architecture:** 使用官方初始化器生成标准 Skill 骨架，只保留 `SKILL.md` 和 `agents/openai.yaml`。Skill 正文负责输入识别、双模式选择、身份与构图不变量、内置 ImageGen 编辑流程和非破坏性输出；根目录登记脚本负责写入 `catalog.yaml`。

**Tech Stack:** Markdown、YAML、官方 `skill-creator` 校验器、项目内 Python `.venv` 和既有 `register_skill.py`。

## Global Constraints

- Skill 必须位于 `skills/other/photo-restoration`，分类只能是 `other`。
- 默认使用忠实修复；只有用户明确要求时才使用现代增强、上色或电影风格。
- 必须保持人物身份、五官比例、姿势、服饰、人物数量、构图、背景和年代细节。
- 默认不覆盖原照片；不宣称内置工具实际输出 8K 像素文件。
- 默认使用内置 ImageGen 编辑工具；切换 CLI 需要用户明确同意并说明 API Key 要求。
- `SKILL.md` frontmatter 只包含 `name` 和 `description`。
- 本首版不新增代码脚本，因此没有新增函数需要注释。

---

## File Map

- `skills/other/photo-restoration/SKILL.md`：触发条件、双模式、提示结构、错误处理和输出规则。
- `skills/other/photo-restoration/agents/openai.yaml`：UI 展示名称、短描述和默认调用提示。
- `catalog.yaml`：新增唯一的 `other` 分类索引记录。
- `skills/other/.gitkeep`：由正式 Skill 目录取代并删除。

### Task 1: Initialize The Skill Scaffold

**Files:**
- Create: `skills/other/photo-restoration/SKILL.md`
- Create: `skills/other/photo-restoration/agents/openai.yaml`
- Delete: `skills/other/.gitkeep`

**Interfaces:**
- Produces: 名称为 `photo-restoration`、位于 `skills/other` 的标准 Skill 目录。

- [ ] **Step 1: Run the official initializer**

Run `init_skill.py photo-restoration --path skills/other` with these interface values: `display_name=Photo Restoration`, `short_description=忠实修复老照片并按需现代增强`, and `default_prompt=Use $photo-restoration to restore this old photo while preserving identity and composition.`

Expected: 生成 `skills/other/photo-restoration/SKILL.md` 和 `skills/other/photo-restoration/agents/openai.yaml`。

- [ ] **Step 2: Confirm the generated structure**

Run: `find skills/other/photo-restoration -maxdepth 2 -type d -print | sort`

Expected: 只输出 Skill 根目录和 `agents` 目录。

- [ ] **Step 3: Commit the scaffold**

Run: `git rm skills/other/.gitkeep && git add skills/other/photo-restoration && git commit -m "chore(photo-restoration): 初始化老照片修复 Skill 骨架"`

### Task 2: Implement The Restoration Workflow

**Files:**
- Modify: `skills/other/photo-restoration/SKILL.md`
- Modify: `skills/other/photo-restoration/agents/openai.yaml` only if generated metadata is stale

**Interfaces:**
- Consumes: 用户上传或已在对话中可见的照片编辑目标。
- Produces: `$photo-restoration` 工作流，包含忠实修复和明确要求后的现代增强两条路径。

- [ ] **Step 1: Replace generated placeholders**

将 `SKILL.md` frontmatter 设置为 `name: photo-restoration`，并使用包含这些触发词的英文 description：restore vintage, blurry, faded, scratched, or damaged photographs; repair an old photo; remove scratches or stains; recover faded detail; sharpen a blurry picture; colorize a black-and-white photo; give a restored photo a modern look。

- [ ] **Step 2: Write the preservation-first workflow**

正文必须明确：默认忠实修复；明确要求现代化、上色或电影感时才启用现代增强；输入图片标记为编辑目标；本地图片先用 `view_image` 加载；人物身份、五官比例、年龄、表情、发型、姿势、服饰、人数和视线不变；主体位置、裁切、宽高比、背景、文字、年代和历史细节不变；默认禁止改脸、磨皮美化、添加人物、改变构图、虚构大面积细节和默认上色。

- [ ] **Step 3: Add ImageGen prompt scaffolding**

提示结构必须包含 `Use case`、`Primary request`、`Input images`、`Restoration`、`Constraints` 和 `Avoid`。有人物时使用 `identity-preserve`，无人物或局部损伤修补时使用 `precise-object-edit`。明确说明“8K”只能作为高细节目标，不代表实际像素输出。

- [ ] **Step 4: Add failure handling and scope boundaries**

说明没有输入图片、关键区域完全缺失、身份漂移、内置工具不可用、用户要求精确分辨率时的处理；明确首版不实现批量修复、传统确定性算法、人工蒙版、面部识别和独立放大脚本。切换 CLI 前必须得到用户明确同意并说明 API Key 要求。

- [ ] **Step 5: Run content checks**

Run `rg -n 'TODO|TBD|\\[TODO' skills/other/photo-restoration || true` and `rg -n '忠实修复|现代增强|identity-preserve|precise-object-edit|view_image|image_gen|不覆盖|8K' skills/other/photo-restoration/SKILL.md`.

Expected: 第一条无输出；第二条找到双模式、输入图像、工具和输出边界内容。

- [ ] **Step 6: Validate and commit the workflow**

Run `.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/other/photo-restoration` and expect `Skill is valid!`. Then run `git add skills/other/photo-restoration && git commit -m "feat(photo-restoration): 增加老照片双模式修复工作流"`.

### Task 3: Register And Verify The Catalog Entry

**Files:**
- Modify: `catalog.yaml`

**Interfaces:**
- Consumes: 已通过官方校验的 `skills/other/photo-restoration`。
- Produces: 唯一索引记录 `name=photo-restoration`、`category=other`、`path=skills/other/photo-restoration`。

- [ ] **Step 1: Register the Skill**

Run `register_skill.py --catalog catalog.yaml --root . --name photo-restoration --category other --path skills/other/photo-restoration --description '忠实修复老照片并按需提供现代增强'` and expect `Registered photo-restoration as other`.

- [ ] **Step 2: Verify the catalog entry**

Use PyYAML to assert exactly one `photo-restoration` record, category `other`, path `skills/other/photo-restoration`, and an existing directory. Print `photo-restoration catalog entry: ok`.

- [ ] **Step 3: Run existing tests and final checks**

Run `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, and `git status --short --branch`. Expect 10 existing tests to pass and no whitespace errors.

- [ ] **Step 4: Commit the catalog update**

Run `git add catalog.yaml && git commit -m "feat(catalog): 登记 photo-restoration 到其他类"`.
