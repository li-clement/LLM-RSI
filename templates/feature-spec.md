# Feature Spec 模板（RSI：循环规格）

```markdown
---
id: F-<year>-<num>
title: 一个完整的改进循环（<目标维度>）
epic: E-<num>
status: draft            # draft → in-review → approved → frozen → released
frozen_at: null
bu: [DATA, MODEL]        # 涉及的消费团队按需加（如 AGENT）
contracts: [<ID>.v<N>]   # 本轮要冻结的全部契约
knowledge: [<知识项ID>]  # 开跑前必须消费的 ADR/PAT/PIT/CARD/RB（负结果尤其）
owner: "@<cycle-owner>（两团队轮值）"
---

# F-<year>-<num> <标题>

## 循环规格
- **目标维度**：<指标 ID + 达标线>（定义只引用 EVAL-* 契约 ID，禁止复述）
- **回归地板**：guard 维度回归数 = 0（列出 guard 清单，引用契约）
- **预算**：算力 ≤ <上轮 x 倍数>；线上成本 ≤ champion x <倍数>；合成占比 ≤ <上限>
- **循环期限**：frozen 后 <N> 天（到期未过 G3 → 循环作废归档）

## 跨团队职责切分
| 工作项 | 责任团队 | 交付物 | 验收锚点 |
|---|---|---|---|
| ... | DATA/MODEL/AGENT | <契约实现/批次/注册记录> | S-xxx |

> 冻结谈判的核心：**先划裁判权与边界，再谈数据格式**。职责切分表未获各方确认前，不得进入 in-review。

## 契约要点
- 只引用契约 ID + 一句意图说明，**禁止复述字段与阈值**（单一事实源）。

## 非目标
- 一轮只动一个目标维度；不改评测基准构成；**不含自动阈值调优——禁止**。

## 风险与知识消费
- <坑点 ID + 一句话对策>；上轮负结果：<ID + 本轮如何避开>

## 验收
- 列出全部关联 Scenario ID；≥1 个 acceptance 场景。
```

## 质量自检（进入 in-review 前）

- [ ] `bu` 中每个团队都有能力卡；`contracts` 引用的契约已存在（或同 PR 新建）
- [ ] 目标维度与 guard 维度都可在 EVAL 契约中解析出指标 ID
- [ ] 职责切分表各方 Steward 已评论确认
- [ ] 非目标至少 3 条（写不出说明还没想清楚这轮不干什么）
- [ ] `python3 tools/check.py` 绿
