# 上下文提交规范

提交记录需要保留代码差异无法说明的意图、取舍、约束和经验。简单修改只写清晰标题；有实际背景时，才增加结构化正文。此规范合并了原 `contextual-commit` Skill。

## 格式和语言

标题遵循 Conventional Commits：

```text
type(scope): 中文摘要

action-type(scope): 中文背景说明
action-type(scope): 另一条有价值的上下文
```

- `type` 保留标准英文值，如 `feat`、`fix`、`refactor`、`test`、`docs`、`chore`；scope 使用项目已有模块名称，并在相同概念上保持一致。
- 标题冒号之后、正文每条冒号之后均用中文。已有技术专有名词可保留原文；只有用户在当前任务中明确要求其他语言时才改变。
- 一条提交只描述其实际包含的改动。正文仅写差异中看不出的信息；通常 1 到 3 条足够，没有真实背景时可以没有正文。
- `action-type(scope): ...` 只能出现在正文，不放进标题。需要重大不兼容变更时仍遵循 Conventional Commits 的 `BREAKING CHANGE` footer。

## 可用的上下文类型

按实际情况选择，不为填满类型而编造：

- `intent(scope)`: 用户希望实现的目标及原因，尽量保持用户原意。
- `decision(scope)`: 多种合理方案中选择了哪一种，以及选择依据。
- `rejected(scope)`: 明确考虑过但放弃的方案，以及放弃原因。
- `constraint(scope)`: 影响实现方式的硬约束、兼容边界或外部限制。
- `learned(scope)`: 实施中发现、能帮助后续维护者避免重复摸索的事实。

例如：

```text
feat(auth): 增加 Google 登录

intent(auth): 用户先接入 Google 登录，后续再支持其他提供方
decision(auth): 沿用现有会话存储，避免引入第二套认证状态
constraint(auth): 回调地址必须兼容已有客户端配置
```

修复错别字、简单格式调整等提交，标题足够时不加空泛正文。

## 提交消息核对

按 [提交前多代理审查](pre-commit-review.md) 核对最终暂存范围，再确保标题和正文仅描述实际提交的改动。`intent`、`rejected`、`constraint`、`learned` 须有本次对话或验证记录支撑；仅凭代码差异可确认技术选型时，可以写 `decision`，不能从结果反推用户动机或未采用方案。

普通 merge、squash、rebase 和 cherry-pick 都可能保留或组合提交正文。提交正文必须独立准确，不依赖当前会话的口头解释。
