# AI Agent Skills 管理项目设计

## 目标

初始化当前仓库，用它集中管理后续创建的 AI Agent Skills。项目提供一个 `create-skill` Skill，负责理解新 Skill 的用途、自动分类、生成标准目录、维护索引并执行校验。

项目只保留两个分类：

- `development`：主要交付物是代码或工程配置。
- `other`：主要交付物不是代码。

## 目录结构

```text
.
├── AGENTS.md
├── README.md
├── catalog.yaml
└── skills
    ├── development
    │   └── create-skill
    │       ├── SKILL.md
    │       ├── agents
    │       │   └── openai.yaml
    │       └── scripts
    │           └── register_skill.py
    └── other
```

`AGENTS.md` 让仓库中的 Agent 在收到新增或修改 Skill 的需求时先读取 `create-skill`。`README.md` 说明项目用途、分类规则和使用方式。`catalog.yaml` 是仓库内全部 Skills 的机器可读索引。

## 分类规则

分类以主要交付物为准，不以主题名称为准。

以下内容归入 `development`：

- 创建或修改源代码、脚本、测试代码。
- 实现 API、数据库结构或数据迁移。
- 维护构建、依赖、持续集成或部署配置。
- 调试程序、审查代码或执行软件工程流程。

写作、翻译、生活、学习、研究、办公、设计和其他不以代码为主要交付物的内容归入 `other`。

混合任务按主要目标分类。核心目标是实现软件功能时归入 `development`；代码只是辅助工具时归入 `other`。如果两类都无法明确占主导，创建前向用户确认。

## 创建流程

1. 读取用户描述，整理 Skill 的目标、触发场景和预期产物。
2. 生成符合规范的短名称，目录名使用小写字母、数字和连字符。
3. 根据主要交付物判断 `development` 或 `other`，并向用户说明判断结果。
4. 分类明确时直接继续；存在实质歧义时请求确认。
5. 使用官方 Skill 初始化脚本生成 `SKILL.md` 和 `agents/openai.yaml`。
6. 仅按实际需要添加 `scripts/`、`references/` 或 `assets/`。
7. 检查关键代码注释和函数文档注释，遵守项目 `AGENTS.md`。
8. 运行 Skill 校验脚本，通过后更新 `catalog.yaml`。

## 索引格式

`catalog.yaml` 保持最小字段集：

```yaml
version: 1
skills:
  - name: create-skill
    category: development
    path: skills/development/create-skill
    description: 创建、分类、登记并校验项目中的 AI Agent Skills
```

Skill 的触发规则只写在自身 `SKILL.md` 的 `description` 中。索引中的描述用于浏览和检索，不替代 Skill 元数据。

## 错误处理

- 名称不符合规范时，先规范化；规范化后为空则停止并请用户补充名称。
- 目标目录已存在时，不覆盖文件，先判断是更新已有 Skill 还是更换名称。
- `catalog.yaml` 已有同名或同路径记录时，拒绝重复登记。
- 分类值只能是 `development` 或 `other`。
- Skill 校验失败时不更新索引，修复后重新校验。
- 脚本采用临时文件和原子替换更新索引，避免写入中断造成半成品。

## 验证

实现阶段至少覆盖以下检查：

- Skill 目录、YAML frontmatter 和名称通过官方快速校验。
- 登记脚本能新增合法 Skill。
- 重复名称、重复路径和非法分类会失败，且不修改索引。
- `catalog.yaml` 中的每个路径都存在，每个 Skill 都被登记一次。
- 使用一个开发类示例和一个其他类示例走通分类与创建流程。

## 边界

首版不增加子分类、标签系统、Web 管理界面或全局安装同步。将来 Skills 数量增加后，可以在不改变两类目录的前提下扩展索引字段。
