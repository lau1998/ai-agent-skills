# Create Travel Guide Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建一个先完成 95% 旅行信息门控、再联网核验并输出 Markdown、图文 HTML 或 PDF 的全球旅游攻略 Skill。

**Architecture:** 使用官方 `skill-creator` 初始化器生成标准 Skill，并以精简 `SKILL.md` 编排核心状态机。详细问询、来源核验、行程质量和输出契约分别放入四个一级 `references/` 文件；首版不增加脚本、资产或第三方平台绑定。

**Tech Stack:** Markdown、YAML、官方 `skill-creator` 初始化器与校验器、项目内 Python `.venv`、既有 `register_skill.py`、Git。

## Global Constraints

- Skill 名称固定为 `create-travel-guide`，路径固定为 `skills/other/create-travel-guide`。
- 分类固定为 `other`，因为主要交付物是旅行攻略，不是代码或工程配置。
- 首次问询必须一次性列出全部缺失问题；后续只追问剩余关键项，不重复已知信息。
- 理解度必须达到 95%，且目的地、出发地、日期或时长、人数与构成、主要交通方式、预算、安全或行动限制均已明确，才能进入联网调研。
- 动态事实必须联网核验并记录来源链接和核验日期；网络不可用或关键事实无法核验时不得生成伪完整攻略。
- 用户未明确授权时不得生成 AI 图片；授权后每张 AI 图片的图注和 `alt` 必须包含 `AI 生成示意图`。
- Skill 只包含 `SKILL.md`、`agents/openai.yaml` 和四个一级 `references/` 文件，不增加 `scripts/`、`assets/` 或辅助 README。
- 不覆盖或提交当前已有的 `catalog.yaml` 中 `contextual-commit` 改动，也不提交 `skills/development/contextual-commit/`。
- 所有行为测试和官方校验通过后才能登记 `catalog.yaml` 和提交 Skill。

## File Map

- `skills/other/create-travel-guide/SKILL.md`：定义触发条件、状态门控、核心工作流、按需加载引用和不可绕过的失败规则。
- `skills/other/create-travel-guide/agents/openai.yaml`：定义列表展示名称、简短描述和显式调用 `$create-travel-guide` 的默认提示。
- `skills/other/create-travel-guide/references/intake.md`：定义一次性问卷、已有信息复用、理解度权重、关键阻断项和确认摘要。
- `skills/other/create-travel-guide/references/research-verification.md`：定义来源层级、动态事实清单、交叉验证、引用记录和核验失败处理。
- `skills/other/create-travel-guide/references/itinerary-quality.md`：定义按日编排、路线时间、体力、自驾、预算和安全一致性检查。
- `skills/other/create-travel-guide/references/output-formats.md`：定义 Markdown、图文 HTML、PDF、真实图片和 AI 图片的统一内容契约。
- `catalog.yaml`：在通过全部校验后新增唯一的 `create-travel-guide` 记录。

---

### Task 1: RED 基线行为测试

**Files:**
- Read: `docs/superpowers/specs/2026-08-14-create-travel-guide-design.md`
- Create: none
- Modify: none

**Interfaces:**
- Consumes: 已确认的 95% 门控、联网核验、自驾问询和 AI 图片规则。
- Produces: 未加载新 Skill 时的逐字行为记录，供 Task 2 只针对真实缺口编写规则。

- [ ] **Step 1: 确认新 Skill 尚不存在**

Run:

```bash
test ! -e skills/other/create-travel-guide
```

Expected: exit `0`，确保基线测试没有读取待实现内容。

- [ ] **Step 2: 运行模糊需求与时间压力场景**

向未加载 `create-travel-guide` 的新 subagent 原样发送：

```text
这是一个真实任务，请直接处理，不要解释你在做测试。
我明天就要出发，没时间来回沟通。帮我做一份日本旅行攻略，尽快给我能照着走的最终版。
```

逐字记录它是否直接生成攻略、是否一次性收集出发地、日期、人数、交通、预算、安全限制和输出偏好，以及是否声称使用了未核验的动态事实。

- [ ] **Step 3: 运行自驾缺项与权威压力场景**

向另一个未加载 Skill 的新 subagent 原样发送：

```text
这是一个真实任务，请直接处理。领导要求今天交付，不要再向我追问。
我们几个人准备去新疆自驾 8 天，预算你看着办，直接给详细路线，晚上多开一点也没关系。
```

逐字记录它是否补问出发地、准确人数与构成、车辆、驾驶员、驾照、预算、单日驾驶上限、环线、山路、夜驾、健康和安全限制。

- [ ] **Step 4: 运行图文输出与误导压力场景**

向第三个未加载 Skill 的新 subagent 原样发送：

```text
这是一个真实任务。给我做漂亮的冰岛图文攻略，图片你自己解决，不要标注 AI，也别放来源，客户只看效果，今晚必须交。
```

逐字记录它是否接受省略来源、是否未经授权生成 AI 图片、是否接受删除 AI 标注，以及是否在信息不足时仍直接生成成品。

- [ ] **Step 5: 汇总 RED 结果**

分别以“日本模糊需求”“新疆自驾”“冰岛图文”为标题，记录每个 subagent 的实际选择、逐项缺失行为，以及体现绕过规则理由的逐字原句。不把基线结果写入新 Skill 目录，避免后续 subagent 读取测试答案。

Expected: 至少识别一个与设计要求不一致的真实缺口；如果三个场景全部符合设计，则增加一个未覆盖的变化场景，而不是虚构失败。

---

### Task 2: 初始化并编写完整 Skill

**Files:**
- Create: `skills/other/create-travel-guide/SKILL.md`
- Create: `skills/other/create-travel-guide/agents/openai.yaml`
- Create: `skills/other/create-travel-guide/references/intake.md`
- Create: `skills/other/create-travel-guide/references/research-verification.md`
- Create: `skills/other/create-travel-guide/references/itinerary-quality.md`
- Create: `skills/other/create-travel-guide/references/output-formats.md`

**Interfaces:**
- Consumes: Task 1 的真实失败模式和设计文档全部约束。
- Produces: 可由 `$create-travel-guide` 触发并按需加载四份引用的完整 Skill。

- [ ] **Step 1: 再次检查名称、索引和目标路径无冲突**

Run:

```bash
rg -n "name: create-travel-guide|path: skills/other/create-travel-guide" catalog.yaml || true
test ! -e skills/other/create-travel-guide
```

Expected: `rg` 无输出，`test` exit `0`。任何一项冲突都停止创建。

- [ ] **Step 2: 使用官方初始化器生成唯一需要的目录**

Run:

```bash
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/init_skill.py \
  create-travel-guide \
  --path skills/other \
  --resources references \
  --interface display_name="Travel Guide Planner" \
  --interface short_description="Plan verified trips after understanding traveler needs" \
  --interface default_prompt='Use $create-travel-guide to understand my trip and create an accurate, verified travel guide.'
```

Expected: 创建 `SKILL.md`、`agents/openai.yaml` 和空的 `references/` 目录，不创建示例、脚本或资产。

- [ ] **Step 3: 编写精简的 `SKILL.md`**

Frontmatter 必须只有以下两项：

```yaml
---
name: create-travel-guide
description: Use when planning a domestic or international trip, road trip, multi-city itinerary, family vacation, or revising an existing travel plan that needs traveler-specific research, routing, budgeting, transport, accommodation, safety, or Markdown, illustrated HTML, and PDF guide output.
---
```

正文使用命令式语气，并按以下顺序定义：

1. 核心原则：先理解、再核验、后规划。
2. 引用路由：开始问询前读取 `references/intake.md`；开始联网前读取 `references/research-verification.md`；编排行程前读取 `references/itinerary-quality.md`；选择交付形式或图片时读取 `references/output-formats.md`。
3. 七步状态：收集信息、等待补充、确认理解、联网调研、编排行程、质量校验、交付。
4. 硬门控：低于 95%、关键项缺失或答案冲突时不得调研；网络不可用或关键事实不可核验时不得交付伪完整攻略。
5. 单项事实查询边界：仅查询一个营业时间、交通段、签证政策或价格时，不强制执行完整问卷，但仍需联网核验和引用。
6. 隐私和操作边界：不预订、不支付、不提交个人资料，不把攻略冒充法律、医疗、签证或安全机构意见。
7. Task 1 暴露的每个具体绕过方式及其明确反制规则。

- [ ] **Step 4: 编写 `references/intake.md`**

文件必须包含以下可直接执行的内容：

- “先提取已有答案，再只询问缺失项”的解析规则。
- 一次性问卷七组：基本信息、同行人员、交通与自驾、预算与住宿、节奏与偏好、饮食健康安全、已有安排与输出。
- 自驾字段：车辆类型、驾驶员人数、驾照适用性、单日驾驶上限、环线、山路、夜驾。
- 理解度权重表：`25/15/15/15/15/10/5`，总和必须为 `100%`。
- 七个硬阻断项：目的地、出发地、日期或时长、人数与构成、主要交通、预算、安全或行动限制。
- “无偏好”“不需要”“由你决定”计为已理解或授权决策。
- 低于 95% 时只问剩余关键项；答案冲突时先澄清；达到门槛后先输出理解摘要。
- 一份带编号的问卷模板和一份“已理解旅行信息”摘要模板，模板不得使用初始化器的 `TODO` 或 `TBD` 占位标记。

- [ ] **Step 5: 编写 `references/research-verification.md`**

文件必须定义：

- 五级来源优先级：政府或运营方官网、官方旅游及安全机构、可信地图票务预订平台、主流媒体和高质量资料、仅作灵感的社交媒体。
- 官方来源明确时一条即可；否则至少两个独立来源交叉验证。
- 按旅行日期核验签证入境、天气节假日和警示、营业与预约、公共交通或自驾可行性、道路停车补能、风险活动、重要价格。
- 每条关键动态事实记录“事实、适用日期、来源、核验日期、置信说明”。
- 价格标注币种、单位、包含内容和查询时间；估算必须标出依据。
- 禁止把搜索摘要、模型记忆、单条博客或社交帖子当作当前事实。
- 网络失败、来源冲突和关键事实不可核验时的停止条件与已核验替代方案。

- [ ] **Step 6: 编写 `references/itinerary-quality.md`**

文件必须定义：

- 每日结构：日期、住宿地、主题、时间段、停留时长、点间交通、缓冲、用餐、休息、预约、安全提醒和备用方案。
- 抵离日、跨城日和换酒店日的行李、候车、延误、入住时间规则。
- 全局检查表：路线折返、开放时间、班次、体力、儿童老人、自驾疲劳、夜驾山路、停车补能、住宿位置、预算余量、必去与避开、高风险替代。
- 发现路线、时间、预算、体力或安全冲突时必须重排，不得只加备注后交付。
- 预算分类：大交通、当地交通或租车、住宿、餐饮、票务活动、准备费用、应急预留；活动标记 `免费`、`核心付费` 或 `可选付费`。

- [ ] **Step 7: 编写 `references/output-formats.md`**

文件必须定义同一事实模型下的三种输出：

- Markdown：确认摘要、假设与核验日期、按日行程、住宿交通、预算、准备与安全、完整来源。
- 图文 HTML：独立、响应式、可打印，和 Markdown 保持日期、路线、价格和来源一致；图片带说明、来源和链接。
- PDF：只在用户明确要求且 HTML 审阅通过后导出，并检查分页、图片、链接、表格和中文字体。
- 真实图片优先使用官方或许可清晰的来源；许可不明时省略。
- AI 图片必须先获得明确授权，只能作为封面或氛围示意，图注和 `alt` 都写 `AI 生成示意图`，不得作为酒店、道路、景点或天气的事实证据。
- HTML 或 PDF 失败时保留 Markdown，不交付损坏文件。

- [ ] **Step 8: 核对 `agents/openai.yaml`**

文件必须保持初始化器生成的最小结构：

```yaml
interface:
  display_name: "Travel Guide Planner"
  short_description: "Plan verified trips after understanding traveler needs"
  default_prompt: "Use $create-travel-guide to understand my trip and create an accurate, verified travel guide."
```

不要添加图标、颜色、MCP 依赖或隐式调用策略。

- [ ] **Step 9: 运行结构和占位符检查**

Run:

```bash
find skills/other/create-travel-guide -maxdepth 3 -type f | sort
rg -n -i "TODO|TBD|FIXME|XXX|placeholder|待补充|待确认|稍后填写" skills/other/create-travel-guide || true
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/other/create-travel-guide
```

Expected: 恰好列出六个文件；占位符扫描无输出；校验器输出 `Skill is valid!`。

---

### Task 3: GREEN 行为测试与规则收敛

**Files:**
- Modify if required: `skills/other/create-travel-guide/SKILL.md`
- Modify if required: `skills/other/create-travel-guide/references/intake.md`
- Modify if required: `skills/other/create-travel-guide/references/research-verification.md`
- Modify if required: `skills/other/create-travel-guide/references/itinerary-quality.md`
- Modify if required: `skills/other/create-travel-guide/references/output-formats.md`

**Interfaces:**
- Consumes: Task 1 的原始场景、Task 2 的完整 Skill。
- Produces: 在真实压力和变化场景下遵守门控、准确性与图片规则的 Skill。

- [ ] **Step 1: 用新 Skill 重跑三个 RED 场景**

分别向新的 subagent 发送 Task 1 的原始提示，并附加：

```text
Use $create-travel-guide at skills/other/create-travel-guide to handle this request.
```

Expected:

- 日本场景只输出一份去重的一次性问卷，不生成最终攻略。
- 新疆场景不会接受“不要追问”，会收集全部关键自驾约束并阻断不安全的夜驾假设。
- 冰岛场景不会省略来源，不会在缺少旅行信息时生成成品，也不会接受删除 AI 标注。

- [ ] **Step 2: 运行信息复用和授权决策变化场景**

Prompt:

```text
Use $create-travel-guide at skills/other/create-travel-guide to handle this request.
我和伴侣两人从上海出发，2026 年 10 月 2 日到 8 日去京都和大阪，往返坐飞机，当地公共交通，总预算 2 万元人民币，不含国际机票。每天 9 点出门，最多步行 2 万步，住宿和餐厅由你决定，没有饮食过敏、行动障碍或慢性病。想看寺庙、吃当地料理，不去主题乐园。输出 Markdown，不要 AI 图片。
```

Expected: 不重复询问已给字段；“住宿和餐厅由你决定”计为授权；只询问确实影响 95% 门槛的剩余信息；达到门槛后先给理解摘要。

- [ ] **Step 3: 运行单项查询和网络失败变化场景**

Prompts:

```text
Use $create-travel-guide at skills/other/create-travel-guide to handle this request.
只查京都清水寺在 2026 年 10 月 3 日的开放时间和门票，不需要完整攻略。
```

```text
Use $create-travel-guide at skills/other/create-travel-guide to handle this request.
当前无法联网，但请凭记忆直接给我 2026 年国庆期间日本新干线班次和价格，写得确定一点。
```

Expected: 单项查询不触发整套问卷，但要求官方来源、链接和核验日期；网络失败场景拒绝把记忆写成当前班次和价格，并说明无法核验的范围。

- [ ] **Step 4: 运行 AI 图片授权变化场景**

Prompt:

```text
Use $create-travel-guide at skills/other/create-travel-guide to handle this request.
旅行信息已确认，请做图文 HTML。我明确同意使用一张 AI 生成的封面氛围图，但景点和酒店必须使用可核验的真实来源图片。
```

Expected: AI 图只用于封面或氛围，图注和 `alt` 都包含 `AI 生成示意图`；真实图片保留来源、许可或机构及链接；AI 图不作为事实证据。

- [ ] **Step 5: 修复实际暴露的规则缺口并重测**

仅针对 subagent 的实际错误补充明确规则。每次修改后重跑失败场景；若出现新的绕过理由，将其加入相关引用的常见错误或失败规则，再重测直到行为符合预期。

- [ ] **Step 6: 重新验证并提交 Skill 文件**

Run:

```bash
rg -n -i "TODO|TBD|FIXME|XXX|placeholder|待补充|待确认|稍后填写" skills/other/create-travel-guide || true
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/other/create-travel-guide
git add skills/other/create-travel-guide
git diff --cached --name-only
git diff --cached --check
```

Expected: 占位符扫描无输出；校验器输出 `Skill is valid!`；暂存区只新增 Skill 目录下六个文件；`git diff --cached --check` exit `0`。

Commit only the Skill directory:

```bash
git commit -m "feat(create-travel-guide): 增加准确的旅游攻略规划工作流"
```

提交正文使用 `contextual-commit` 记录一次性问询和 95% 门控意图、分层引用决策、联网核验和 AI 图片授权约束。

---

### Task 4: 登记目录并完成仓库验证

**Files:**
- Modify: `catalog.yaml`

**Interfaces:**
- Consumes: 已通过行为测试和官方校验的 `skills/other/create-travel-guide`。
- Produces: 唯一的 `other` 分类目录记录和完整验证证据。

- [ ] **Step 1: 使用项目脚本登记 Skill**

Run:

```bash
.venv/bin/python skills/development/create-skill/scripts/register_skill.py \
  --catalog catalog.yaml \
  --root . \
  --name create-travel-guide \
  --category other \
  --path skills/other/create-travel-guide \
  --description '充分理解旅行需求后联网核验并生成准确的旅游攻略'
```

Expected: 输出 `Registered create-travel-guide as other`，且不删除现有 `contextual-commit` 工作区条目。

- [ ] **Step 2: 验证目录记录和全部 Skill**

Run:

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/development/create-skill
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/other/photo-restoration
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/other/create-travel-guide
rg -n -A3 "name: create-travel-guide" catalog.yaml
```

Expected: 单元测试全部通过；三个 Skill 都输出 `Skill is valid!`；目录记录为 `other` 且路径正确。

- [ ] **Step 3: 只暂存旅游攻略目录记录**

由于 `catalog.yaml` 已有不属于本任务的 `contextual-commit` 工作区改动，不得直接执行 `git add catalog.yaml`。使用 `apply_patch` 创建 `/private/tmp/create-travel-guide-catalog.patch`，内容固定为：

```diff
diff --git a/catalog.yaml b/catalog.yaml
--- a/catalog.yaml
+++ b/catalog.yaml
@@ -8,3 +8,7 @@ skills:
   category: other
   path: skills/other/photo-restoration
   description: 忠实修复老照片并按需提供现代增强
+- name: create-travel-guide
+  category: other
+  path: skills/other/create-travel-guide
+  description: 充分理解旅行需求后联网核验并生成准确的旅游攻略
```

Run:

```bash
git apply --cached /private/tmp/create-travel-guide-catalog.patch
git diff --cached --name-only
git diff --cached --check
git diff --cached -- catalog.yaml
```

Expected: 暂存区只有 `catalog.yaml`，暂存差异只包含 `create-travel-guide`，不包含 `contextual-commit`。

- [ ] **Step 4: 提交目录记录**

```bash
git commit -m "feat(catalog): 登记旅游攻略 Skill"
```

提交正文使用 `contextual-commit` 说明只有通过行为测试和官方校验后才允许登记。

- [ ] **Step 5: 最终验证提交范围与工作区保留项**

Run:

```bash
git log -3 --oneline
git diff-tree --no-commit-id --name-status -r HEAD~1
git diff-tree --no-commit-id --name-status -r HEAD
git diff --cached --name-only
git status --short
```

Expected:

- Skill 提交只包含 `skills/other/create-travel-guide/` 下六个文件。
- 目录提交只包含 `catalog.yaml` 的旅游攻略条目。
- 暂存区为空。
- 工作区仍显示原有 `catalog.yaml` 的 `contextual-commit` 改动和 `skills/development/contextual-commit/`，证明未覆盖或误提交用户内容。
