# Spec 平面规则（RSI 项目适配）

Spec 平面承载**跨团队的意图与口径**。一切 DATA↔MODEL↔AGENT 的协作只认这里的定点契约，不认实验脚本里的内联定义、聊天记录或口头承诺（单一事实源原则）。

## 工件链

```
E ──► F（循环规格）──► Contract（五类，机器可读 JSON）
                       └► Scenario（acceptance 验收 / contract 契约断言）
```

引用方向是单向咬合：Feature 引用 Contract 与 Knowledge 的 ID；Scenario 引用 Feature 或 Contract 的 ID；Contract 内用 `x-contract.consumers` 声明消费方团队。任何环引用视为设计错误。

## ID 与命名（check.py 强制）

| 工件 | ID | 文件名 | 位置 |
|---|---|---|---|
| Epic | `E-<num>` | `E-001-<slug>.md` | `specs/epics/` |
| Feature | `F-<year>-<num>` | `F-2026-001-<slug>.md` | `specs/features/` |
| Contract | `<域码>-<动作>` | `<ID>.v<major>.<flavor>.json` | `specs/contracts/` |
| Scenario | `S-<num>` | `S-001-<slug>.md` | `specs/scenarios/` |

- 域码 = 提供方域缩写（见 [术语表](../knowledge/domain/CONTEXT.md)）：`TRJ` 轨迹 / `DS` 数据集 / `EVAL` 评测协议 / `MDL` 模型服务。
- flavor ∈ `openapi`(api) / `asyncapi`(event) / `schema`(dataset) / `eval`(评测协议) / `model`(模型契约)。
- 文件名 `v<major>` 必须与 `x-contract.version` 主版本一致。

## 状态机

- Epic / Feature：`draft → in-review → approved → frozen → released`
- Contract：`active → deprecated`（必须带 `sunset` 日期）
- Scenario：无状态，跟随引用方

**RSI 特别条款**：

1. Feature = 一个改进循环的规格。`frozen` 是循环起跑线：mix 口径、评测协议版本、模型接口、轨迹 schema 同时锁定；**循环进行中禁止修改 frozen 契约**——可比性由此而来。
2. `EVAL-*` 契约（kind: eval）：指标定义与阈值的**任何**变更一律按破坏性处理，`x-contract.approval` 必须为 `committee`，只有 RSI 治理委员会可批。
3. 超参数不属于契约——循环内随便调；**口径**属于契约——frozen 后不许动。

## 版本与兼容性策略

1. 每个契约声明 `compatibility`：`backward`（默认）/ `forward` / `bidirectional`。
2. 非破坏：dataset schema 加可选字段、SLA 收紧、API 加可选参数 → minor。
3. 破坏：字段删除/改名、枚举收窄、必填新增、mix 口径变更、评测阈值变化 → 新 major + 旧 `deprecated` + `sunset`（≥90 天双跑）+ CR。
4. 每个契约必须 ≥1 个契约场景；每个 Feature 必须 ≥1 个验收场景——**没有断言的数据集不是资产，是负债**。

## 冻结（G2）操作序列

1. Cycle Owner 提 PR：Feature `approved → frozen`，填 `frozen_at`；
2. Dataset Steward、Eval Steward、Model Steward 与各 consumer 团队代表联签；
3. P1 全绿（check + schema-diff + eval 协议 diff 无未批变更）；
4. 合并即冻结生效，此后一切变更走 CR（模板：[templates/contract-change.md](../templates/contract-change.md)）。
