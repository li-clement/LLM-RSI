# Spec 平面规则

Spec 平面承载**跨 BU 的意图与边界**。一切跨部门协作只认这里的定点契约，不认聊天记录、wiki 复述或口头承诺（单一事实源原则）。

## 工件链

```
E ──► F ──► Contract（api/event/data，机器可读 JSON）
          └► Scenario（acceptance 验收场景 / contract 契约场景）
```

引用方向是**单向咬合**：Feature 引用 Contract 与 Knowledge 的 ID；Scenario 引用 Feature 或 Contract 的 ID；Contract 内部用 `x-contract.consumers` 声明消费方 BU。任何环引用视为设计错误。

## ID 与命名（check.py 强制）

| 工件 | ID | 文件名 | 位置 |
|---|---|---|---|
| Epic | `E-<num>` | `E-001-<slug>.md` | `specs/epics/` |
| Feature | `F-<year>-<num>` | `F-2026-001-<slug>.md` | `specs/features/` |
| Contract | `<域码>-<动作>` | `<ID>.v<major>.<flavor>.json` | `specs/contracts/` |
| Scenario | `S-<num>` | `S-001-<slug>.md` | `specs/scenarios/` |

- 域码 = 提供方 BU 的缩写（见术语表的 BU 代码表），如 `ORD`（交易）、`PAY`（支付）。
- flavor ∈ `openapi`（API）/ `asyncapi`（事件）/ `schema`（数据/消息体）。
- 文件名中的 `v<major>` 必须与 `x-contract.version` 主版本一致。

## 状态机

- Epic / Feature：`draft → in-review → approved → frozen → released`
- Contract：`active → deprecated`（deprecated 必须带 `sunset` 日期）
- Scenario：无状态，跟随其引用的 Feature/Contract

状态写在 frontmatter 的 `status:` 字段。**`frozen` 之后修改契约本体的 PR 一律被 CI 拒绝**，只能提 CR（[templates/contract-change.md](../templates/contract-change.md)）。

## 版本与兼容性策略

1. 每个契约声明 `compatibility`：`backward`（默认）/ `forward` / `bidirectional`。
2. 非破坏性变更：同 major 内 minor 递增（改 `x-contract.version` 与 `info.version`）。
3. 破坏性变更：新建 `v<N+1>` 文件；旧文件 status 改 `deprecated` 并填 `sunset`；CR 必须包含双跑/迁移方案与受影响 consumer 清单（由 contract-impact Agent 预生成）。
4. 每个契约必须 ≥1 个 `kind: contract` 的契约场景，否则 G1 失败。
5. 每个 Feature 必须 ≥1 个 `kind: acceptance` 的验收场景。

## 冻结（G2）操作序列

1. Spec Owner 将 Feature 状态改为 `frozen` 并填 `frozen_at`；
2. Contract Steward（提供方）与各 consumer 的 BU 代表在 PR 上联签；
3. P1 流水线跑全量 check + 兼容性 diff 绿；
4. 合并即冻结生效，此后一切变更走 CR。
