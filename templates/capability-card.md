# 能力卡模板（每个 BU 一张，季度复核）

```markdown
---
id: CARD-<num>
type: capability
title: <BU 全称>能力卡
bu: <BU代码>             # 与 CONTEXT.md BU 代码表一致
scope: "bu:<code>"
confidence: high
status: accepted
owner: "@<BU 技术负责人>"
provenance: [<季度盘点标识>]
expires: <YYYY-MM-DD>    # TTL 90d，消费即续约
provides: [<ID>.v<N>]    # 本 BU 作为 owner 的契约
consumes: [<ID>.v<N>]    # 本 BU 作为 consumer 的契约
contact: "#<值班频道>"
---

# <BU> 能力卡

## 负责什么
3–5 条，动词开头。这是别人找你的路由表。

## 边界与非目标
明确拒绝过什么请求（附仲裁来源）。跨部门扯皮时先回这里。

## 提供的契约 / 消费的契约
只列 ID（check.py 校验与契约 x-contract 的双向一致性——能力地图必须等于现实）。

## 消费节奏与能力
发布窗口、灰度策略、契约测试接入状态、值班与 SLA。
```

## 要点

- 能力卡是**新协作方的第一入口**：对方 BU（及其 Agent）据此判断"这事找谁、有没有现成能力"。
- `provides/consumes` 与契约 `x-contract.owner/consumers` 不一致时 CI 报错——这是三平面里最常被玩坏的一组关系，值得机器守住。
- 每季度 Curator + BU 负责人 30 分钟复核；不更新就过期（G1 红）。
