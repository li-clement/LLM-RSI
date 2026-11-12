---
id: PIT-001
type: pitfall
title: 事件 schema 字段删除与枚举收窄是隐形破坏
scope: cross-bu
confidence: high
status: accepted
owner: "@curator-pay"
provenance: [INC-2026-041, ORD-PAID.v1 CR-7]
expires: 2027-05-31
---

# PIT-001 契约"看起来没改"的三类隐形破坏

## 故事

INC-2026-041：ORD-PAID 事件把 `channel` 枚举从 6 值收窄到 4 值，provider 侧测试全绿（它只产 4 值），消费方 FULFILL 遇到存量渠道映射表外数据直接异常，履约停摆 26 分钟。

## 三类隐形破坏（一律视为破坏性变更，无例外）

1. **字段删除/改名**：哪怕"没人用"——消费者可能有映射表、报表、对账在偷偷读；
2. **枚举收窄**：提供方安全 ≠ 消费方安全；
3. **必填新增 / 约束收紧**（minLength、pattern）：存量合法请求会变非法。

## 探测：流水线怎么拦

- P1 契约 diff：oasdiff / json-schema-diff 对每个契约 PR 做 breaking 判定，**工具结论优先于人**；
- compat-reviewer Agent 报告列出每个 consumer 的影响与存量样本回放结果；
- 消费方 CDC 测试（S-003 类场景）必须用**生产采样回放**，不能只用契约示例。

## 预防

需要收窄时：新 major + 旧契约 `sunset` 双跑；消费方确认覆盖后旧事件才停发。
