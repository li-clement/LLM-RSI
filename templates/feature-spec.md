# Feature Spec 模板

```markdown
---
id: F-<year>-<num>
title: <一句话能力描述>
epic: E-<num>
status: draft            # draft → in-review → approved → frozen → released
frozen_at: null
bu: [<BU代码>, <BU代码>]
contracts: [<ID>.v<N>]   # 引用 specs/contracts 中的 ID.vMajor
knowledge: [<知识项ID>]  # 实现本 Feature 必须消费的 ADR/PAT/PIT/CARD/RB
owner: "@<人名>（主责 BU）"
---

# F-<year>-<num> <标题>

## 用户故事
作为<X>，希望<Y>，以便<Z>。（跨 BU 时每方各写一条，冲突处即谈判点）

## 跨 BU 职责切分
| 工作项 | 责任 BU | 交付物 | 验收锚点 |
|---|---|---|---|
| ... | ... | <契约或系统> | S-xxx |

> 冻结谈判的核心：先划边界，再谈接口。职责切分表未获各方确认前，不得进入 in-review。

## 契约要点
- 只引用契约 ID + 一句意图说明，**禁止复述字段**（单一事实源）。

## 非目标
- 本期明确不做什么（防 scope 蔓延，也是拒绝临时加塞的依据）。

## 风险与知识消费
- <已知坑点 ID + 一句话对策>

## 验收
- 列出全部关联 Scenario ID；≥1 个 acceptance 场景。
```

## 质量自检（进入 in-review 前）

- [ ] `bu` 中每个代码都有能力卡；`contracts` 引用的契约已存在（或同 PR 新建）
- [ ] 职责切分表各方负责人已评论确认
- [ ] 非目标至少 2 条（写不出说明还没想清楚）
- [ ] `python3 tools/check.py` 绿
