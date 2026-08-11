# AI Agent Skills

这个仓库用于集中创建和管理 AI Agent Skills。新增 Skill 时，由项目内的 `create-skill` 判断分类、生成标准文件、运行校验并更新目录索引。

## 分类

项目只有两个分类：

- `skills/development/`：主要交付物是源代码、脚本、测试、API、数据库结构、构建配置或部署配置。
- `skills/other/`：主要交付物不是代码，例如写作、翻译、学习、研究、办公和生活类工作流。

混合任务按主要目标判断。核心目标是实现软件功能时归入 `development`；代码仅作为辅助工具时归入 `other`。无法明确判断时，创建前向用户确认。

## 环境准备

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
```

## 常用命令

运行登记脚本测试：

```bash
.venv/bin/python -m unittest discover -s tests -v
```

校验 `create-skill`：

```bash
.venv/bin/python /Users/chard/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/development/create-skill
```

浏览已登记的 Skills：

```bash
sed -n '1,240p' catalog.yaml
```

## 目录索引

`catalog.yaml` 是项目的统一索引。每条记录包含 Skill 名称、分类、相对路径和简介。不要直接追加重复记录，应使用 `create-skill` 提供的登记脚本更新。

