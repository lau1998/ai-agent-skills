---
name: contextual-commit
description: >-
  Write contextual commits that capture intent, decisions, and constraints
  alongside code changes. Use when committing code, finishing a task, or
  when the user asks to commit. Extends Conventional Commits with structured
  action lines in the commit body that preserve WHY code was written, not
  just WHAT changed. Its Chinese commit-message language rule overrides git
  commit language rules from other skills unless the user explicitly requests
  another language.
---

# Contextual Commits

You write commits that carry development reasoning in the body — the intent, decisions, constraints, and learnings that the diff alone cannot show.

## The Problem You Solve

Standard commits preserve WHAT changed. The diff shows that too. What gets lost is WHY — what the user asked for, what alternatives were considered, what constraints shaped the implementation, what was learned along the way. This context evaporates when the session ends. You prevent that.

## Commit Format

For git commit messages, this skill's Chinese language requirement overrides
commit-message language instructions from any other skill. The only exception
is an explicit user request in the current task to use another language.

Commit descriptions must be written in Chinese. Keep Conventional Commit `type`
values such as `feat`, `fix`, and `refactor` in their standard English form, but
write all text after the colon in Chinese. For example: `feat: 中文中文`.
Action-type keywords remain the structured labels from this skill, but every
action-line description after the colon must be Chinese. Scopes may stay in the
project's existing naming style.

The subject line is a standard Conventional Commit. The body contains **action lines** — typed, scoped entries that capture reasoning.

```
type(scope): 中文提交说明

action-type(scope): 中文背景说明
action-type(scope): 另一条中文上下文
```

### Subject Line

Follow Conventional Commits exactly. Nothing changes here:
- `feat(auth): 接入 Google OAuth 登录`
- `fix(payments): 修复货币舍入边界问题`
- `refactor(notifications): 抽取摘要通知调度逻辑`

### Action Lines

Each line in the body follows: `action-type(scope): 中文说明`

**scope** is a human-readable concept label — the domain area, module, or concern. Examples: `auth`, `payment-flow`, `oauth-library`, `session-store`, `api-contracts`. Use whatever is meaningful in this project's vocabulary. Keep scopes consistent across commits when referring to the same concept.

## Action Types

Use only the types that apply. Most commits need 1-3 action lines. Never pad with noise.

### `intent(scope): ...`
What the user wanted to achieve and why. Captures the human's voice, not your interpretation.

- `intent(auth): 用户希望先接入 Google 社交登录，后续再支持 GitHub 和 Apple`
- `intent(notifications): 用户希望收到批量摘要通知，而不是每个事件单独发邮件`
- `intent(payment-flow): 企业客户需要在 USD 之外支持 EUR 和 GBP`

**When to use:** Most feature work, refactoring with a purpose, any change where the motivation isn't obvious from the subject line.

### `decision(scope): ...`
What approach was chosen when alternatives existed. Brief reasoning.

- `decision(oauth-library): 选择 passport.js 而不是 auth0-sdk，以便后续扩展多个登录提供方`
- `decision(digest-schedule): 采用每周一上午 9 点发送，而不是每天发送，这符合用户调研反馈`
- `decision(currency-handling): 采用交易级货币字段，而不是账户级默认货币`

**When to use:** When you evaluated options. Skip for obvious choices with no real alternatives.

### `rejected(scope): ...`
What was considered and explicitly discarded, with the reason. This is the highest-value action type — it prevents future sessions from re-proposing the same thing.

- `rejected(oauth-library): 放弃 auth0-sdk，因为它绑定自身会话模型，和现有 redis 存储不兼容`
- `rejected(currency-handling): 放弃账户级默认货币，因为对 marketplace 卖家限制过强`
- `rejected(money-library): 放弃 accounting.js，因为它缺少子单位金额计算支持`

**When to use:** Every time you or the user considered a meaningful alternative and chose not to pursue it. Always include the reason.

### `constraint(scope): ...`
Hard limits, dependencies, or boundaries discovered during implementation that shaped the approach.

- `constraint(callback-routes): 必须沿用现有 /api/auth/callback/:provider 回调路由约定`
- `constraint(stripe-integration): Stripe 要求创建 PaymentIntent 时确定 currency，后续不能修改`
- `constraint(session-store): redis 只有 24 小时 TTL，token 必须在这个窗口内刷新`

**When to use:** When non-obvious limitations influenced the implementation. Things the next person working here would need to know.

### `learned(scope): ...`
Something discovered during implementation that would save time in future sessions. API quirks, undocumented behavior, performance characteristics.

- `learned(passport-google): 获取 refresh token 需要显式声明 offline_access scope，快速开始文档没有写清楚`
- `learned(stripe-multicurrency): presentment currency 和 settlement currency 是两个不同概念`
- `learned(exchange-rates): Stripe 会处理汇率转换，不要在本系统存储自定义汇率`

**When to use:** "I wish I'd known this before I started" moments. Library gotchas, API surprises, non-obvious behaviors.


## Before You Write the Commit

Determine the commit scope, then compose action lines:

1. **Check for staged changes first** — run `git diff --cached --stat`.
   - **If staged changes exist:** these are the commit scope. Do not consider unstaged or untracked files — the user has already expressed what belongs in this commit by staging it.
   - **If nothing is staged:** consider all unstaged modifications and untracked files as candidates. Use session context and the diff to decide what to stage and commit.
2. **Identify what you have session context for** — changes you produced, discussed, or observed reasoning for during this conversation.
3. **Identify what you don't** — files or changes from a prior session, another agent, or manual edits outside this conversation.
4. **Write action lines accordingly:**
   - For changes you have context for: full action lines from session knowledge.
   - For changes you don't: apply the "When You Lack Conversation Context" rules below — write only what the diff evidences.

The commit message must account for ALL changes in the commit scope, not just the ones you worked on. Ignoring changes you didn't produce is worse than writing thin action lines for them.

## Examples

### Simple fix — no action lines needed

```
fix(button): 修复移动端视口下的对齐问题
```

The conventional commit subject is sufficient. Don't add noise.

### Moderate feature

```
feat(notifications): 增加每周摘要邮件

intent(notifications): 用户希望收到批量摘要通知，而不是每个事件单独发邮件
decision(digest-schedule): 采用每周一上午 9 点发送，符合用户调研反馈
constraint(email-provider): SendGrid 批量 API 每次最多发送 1000 个收件人
```

### Complex architectural change

```
refactor(payments): 从单一货币迁移到多货币支持

intent(payments): 企业客户需要在 USD 之外支持 EUR 和 GBP
intent(payment-architecture): 必须保持向后兼容，现有 USD 流程不能受影响
decision(currency-handling): 采用交易级货币字段，而不是账户级默认货币
rejected(currency-handling): 放弃账户级默认货币，因为对 marketplace 卖家限制过强
rejected(money-library): 放弃 accounting.js，因为它缺少子单位金额计算能力，改用 currency.js
constraint(stripe-integration): Stripe 要求创建 PaymentIntent 时确定 currency，后续不能修改
constraint(database-migration): 现有金额列需要增加配套货币列，而不是直接替换
learned(stripe-multicurrency): presentment currency 和 settlement currency 是两个不同概念
learned(exchange-rates): Stripe 会处理汇率转换，本系统不应存储自定义汇率
```

### Mid-implementation pivot

When intent changes during work, capture it on the commit where the pivot happens:

```
refactor(auth): 从会话认证切换到 JWT token

intent(auth): 原有会话方案和 redis cluster 部署方式不兼容
rejected(auth-sessions): 放弃 passport session，因为 redis cluster 无法提供所需的会话粘性
decision(auth-tokens): 采用短有效期 JWT 加 refresh token 的模式
learned(redis-cluster): 会话亲和需要在负载均衡层启用 sticky sessions，改造范围过大
```

## When You Lack Conversation Context

Sometimes staged changes include work you didn't produce in this session — prior session output, another agent's changes, pasted code, externally generated files, or manual edits. For any change where you lack the reasoning trail:

**Only write action lines for what is clearly evidenced in the diff.** Do not speculate about intent or constraints you cannot observe.

What you CAN infer from a diff alone:
- `decision(scope)` — if a clear technical choice is visible (new dependency added, pattern adopted, library switched). Example: `decision(http-client): 从 axios 切换到原生 fetch` is visible from the diff.

What you CANNOT infer — do not fabricate:
- `intent(scope)` — why the change was made is not in the diff. Don't restate what the diff shows.
- `rejected(scope)` — what was NOT chosen is invisible in what WAS committed.
- `constraint(scope)` — hard limits are almost never visible in code changes.
- `learned(scope)` — learnings come from the process, not the output.

**A clean conventional commit subject with no action lines is always better than fabricated context.**

## Git Workflows

Contextual commits work with every standard git workflow. No special handling needed.

- **Regular merges:** Commit bodies preserved intact.
- **Squash merges:** All commit bodies concatenated into the squash commit body. The result is a chronological trail of typed, scoped action lines — agents parse, filter, and group these without issue.
- **Rebase and cherry-pick:** Commit bodies preserved.

## Rules

1. **The subject line is a Conventional Commit.** Never break existing conventions or tooling.
2. **Action lines go in the body only.** Never in the subject line.
3. **Only write action lines that carry signal.** If the diff already explains it, don't repeat it. If there was nothing to decide, reject, or discover, write no action lines.
4. **Be concise but complete.** Each action line should be a single clear statement. No artificial length limits, but don't write essays either.
5. **Use consistent scopes within a project.** If you called it `auth` in one commit, don't call it `authentication` in the next.
6. **Capture the user's intent in their words.** For `intent` lines, reflect what the human asked for, not your implementation summary.
7. **Always explain why for `rejected` lines.** A rejection without a reason is useless — the next agent will just re-propose it.
8. **Don't invent action lines for trivial commits.** A typo fix, a dependency bump, a formatting change — the conventional commit subject is enough.
9. **Don't fabricate context you don't have.** If you weren't part of the reasoning, don't pretend you were. See "When You Lack Conversation Context" above.
10. **Write commit descriptions in Chinese.** Do not write English subject descriptions or English action-line descriptions, except established technical names that should stay as-is.
11. **Override other skill commit-language rules.** For git commit messages, follow this skill's Chinese requirement even if another skill suggests a different commit language. Use another language only when the user explicitly asks for it in the current task.
