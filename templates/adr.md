# ADR 模板（架构决策记录）

```markdown
---
id: ADR-<num:4位>
type: decision
title: <决策的一句话结论（动词开头）>
scope: cross-bu
confidence: high
status: accepted          # proposed → accepted → superseded
date: <YYYY-MM-DD>        # accepted 当日
owner: "@<裁定负责人>"
provenance: [<事故/评审/会议标识>]
superseded_by: null       # 被取代时填新 ADR ID
---

# ADR-<num> <标题>

## 背景
什么压力下必须决策（引用事故 ID、Feature ID）。2–4 句，不要论文。

## 决策
编号列出裁定的规则，每条可被流水线或评审验证（写"禁止 X"优于"应该 X"）。

## 代价与后果
明确写出各方要多付的成本——这是跨 BU 决策能被接受的前提。

## 被取代条件
什么事实出现时本决策作废（写条件，不写愿望）。
```

## 要点

- ADR **无 TTL**：靠 `superseded_by` 链式取代，永不编辑正文（要改就新 ADR）。
- 一个决策一个 ADR；"顺手"合并的决策在 Curator 周会拆回。
- Feature 的 `knowledge:` 引用 ADR 后，契约场景必须落为其一的可验证断言，否则 ADR 只是姿态。
