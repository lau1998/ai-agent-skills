# 分支命名规范

新建事项分支统一使用 `chard/<类型>/<事项标识>`。类型表示工作目的，不必与提交消息的 Conventional Commit 类型完全相同。用户给出分支名时将其整理为此格式；若原名称表达的类型与需求冲突，先澄清，不擅自改类。无法判断类型时先确认。

- 事项标识优先使用需求号或 Jira 号，如 `2894`；需要说明时在编号后用 `-` 连接简短关键词，如 `2894-berealpay`。没有编号时使用能区分事项的小写关键词。关键词只用小写字母、数字和连字符；Jira 号保留其正式写法。
- 只有修复明确针对 `master` 且没有事项号时，才可在标识中使用 `master-`，如 `chard/fix/master-berealpay`。有事项号时优先使用编号，如 `chard/fix/2894-berealpay`；不得仅因分支从 `master` 创建就加 `master-`。
- 一个分支只对应一个事项。新建前按事项号或其他可识别的事项信息核对本地、远端现存分支及可查询的事项和合并记录，不能只查同名分支；同一事项已有未完成分支时继续使用，或先向用户澄清独立分支的必要性。已完成事项的分支即使已删除也不得复用；如需继续处理，先确认新的事项标识。无法核实完成状态时先确认。

| 类型 | 用途 | 示例 |
| --- | --- | --- |
| `feat` | 新功能或已有功能增强 | `chard/feat/2894` |
| `fix` | 普通缺陷修复 | `chard/fix/2895-berealpay` |
| `hotfix` | 已确认的生产环境紧急故障修复 | `chard/hotfix/payment-timeout` |
| `experiment` | 技术或设计探索，结果未必合并 | `chard/experiment/cache-strategy` |
| `docs` | 仅修改文档 | `chard/docs/api-guide` |
| `refactor` | 不改变外部行为的代码重构 | `chard/refactor/auth-service` |
| `test` | 仅补充或调整测试 | `chard/test/auth-cases` |
| `chore` | 依赖、工具或日常维护 | `chard/chore/update-deps` |
| `ci` | 持续集成流水线配置 | `chard/ci/lint-check` |
| `perf` | 以性能改善为主要目标 | `chard/perf/query` |
| `release` | 版本发布准备 | `chard/release/v1-2-0` |

普通 bug 使用 `fix`；只有故障已发生在生产环境且确实紧急时才使用 `hotfix`。混合任务按主要交付目的选类型；不能判断、或用户给出的类型与任务冲突时先澄清。无论类型如何，基准分支仍按主 Skill 的 `master` 优先规则选择。
