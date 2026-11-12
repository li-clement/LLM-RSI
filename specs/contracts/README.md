# 契约（Contract）规范

契约是 Spec 平面的**硬通货**：机器可读的 JSON 文件，人和 Agent 消费同一份。

## 文件格式

`specs/contracts/<ID>.v<major>.<flavor>.json`

- `openapi`：同步 API，OpenAPI 3.0 文档；
- `asyncapi`：异步事件，AsyncAPI 2.6 文档；
- `schema`：共享数据结构，JSON Schema 2020-12。

元数据内嵌在文档的 `x-contract` 扩展字段中（单一文件即完整事实，无 sidecar）：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` | ✓ | `<域码>-<动作>`，与文件名一致 |
| `kind` | ✓ | `api` / `event` / `data`（必须与 flavor 对应） |
| `version` | ✓ | semver；主版本必须等于文件名 `v<N>` |
| `status` | ✓ | `active` / `deprecated`（后者必须带 `sunset`） |
| `owner` | ✓ | 提供方 BU 代码（如 `MID`） |
| `consumers` | ✓ | 消费方 BU 代码数组（至少 1 个） |
| `compatibility` | ✓ | `backward` / `forward` / `bidirectional` |
| `steward` | ✓ | Contract Steward 的负责人标识 |

## 变更规则速览

1. 非破坏变更：改 `version` 的 minor/patch，PR 由对方 BU 的 Steward 审核。
2. 破坏性变更：新建 `v<N+1>` 文件 + 旧文件转 `deprecated` + `sunset` 日期 ≥ 90 天后；必须附 [CR](../../templates/contract-change.md)。
3. 字段删除/枚举收窄/必填新增 = 破坏性变更，无例外（见 [PIT-001](../../knowledge/pitfalls/PIT-001-event-field-narrowing.md)）。
4. CI（P1）会用 oasdiff / json-schema-diff 类工具做兼容性判定，Agent 报告仅作预分析，**工具结论优先**。

## 当前契约清单

| 契约 | kind | owner | consumers | status |
|---|---|---|---|---|
| ORD-CREATE.v1 | api | MID | FRONT* | active |
| ORD-PAID.v1 | event | MID | PAY, FULFILL | active |
| PAY-CONFIRM.v1 | api | PAY | MID | active |

（* 示例中前端渠道以消费方标注，试点期只计入 BU 级 consumer。）
