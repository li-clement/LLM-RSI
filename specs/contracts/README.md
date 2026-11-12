# 契约（Contract）规范

契约是 Spec 平面的**硬通货**：机器可读 JSON，人和 Agent 消费同一份。RSI 项目共六类：

| kind | flavor（文件后缀） | 承载 | 一句话 |
|---|---|---|---|
| `dataset` | `.schema.json` | 数据集记录 schema + SLA + 质量断言 | 训练食材的安全标准 |
| `event` | `.asyncapi.json` | 轨迹回流事件流 | 循环的"血液"管道 |
| `api` | `.openapi.json` | 同步接口（如有） | 传统接口契约 |
| `eval` | `.eval.json` | 评测协议：基准/指标/阈值/隔离 | **循环的裁判** |
| `model` | `.model.json` | 模型服务契约：签名/预算/降级/失效清单 | 成品的说明书 |
| `metric` | `.metric.json` | 指标契约：口径/单位/SLO/告警/采集点 | **循环的仪表盘刻度**（dashboard-as-code 的事实源） |

## 文件格式

`specs/contracts/<ID>.v<major>.<flavor>.json`，元数据内嵌在文档的 `x-contract` 字段（单文件即完整事实）：

| 字段 | 必填 | 说明 |
|---|---|---|
| `id` / `kind` / `version` / `status` / `owner` / `consumers` / `compatibility` / `steward` | ✓ | 见 specs/README.md 规则 |
| `approval` | eval 必填 | 固定 `committee`——阈值冻结权在治理委员会 |

各 kind 的额外必填扩展（check.py 校验）：

- `dataset`：`x-sla`（cadence / freshness_days / min_count）+ `x-quality`（≥1 条可执行断言，必须含污染审计条目）；
- `eval`：`x-protocol`（benchmark / metrics / thresholds / isolation 四节齐全）；
- `model`：`x-signature`（input/output）+ `x-budget` + `x-fallback`；
- `metric`：`x-telemetry.collect`（发射点绑定）+ `x-telemetry.metrics[]`（每条必有 id/def/unit；无 `slo` 必须标 `informational: true`；指标 ID 全局唯一，跨契约重复即违反单一事实源）；
- `event` / `api`：本体即标准 spec，无额外扩展。

`metric` 契约与仪表盘联动：`observability/dashboards/*.board.json` 的面板与告警只能引用已注册指标 ID，check.py 自动校验（裸名指标禁止）。

## 变更规则速览

1. 非破坏变更：minor 递增，对方 Steward 审核。
2. 破坏性变更：新 `v<N+1>` 文件 + 旧转 `deprecated` + `sunset` ≥90 天后 + CR（含双跑与波及清单）。
3. **评测协议例外**：阈值与指标定义变更，无论 schema 是否兼容，一律破坏性 + 委员会批准——防"换尺子"是本模式在 RSI 场景的第一优先级（见 PIT-001）。
4. CI（P1）用 schema-diff / oasdiff 类工具判定兼容性，**工具结论优先于人**；Agent 报告仅作预分析。

## 当前契约清单

| 契约 | kind | owner | consumers | status |
|---|---|---|---|---|
| TRJ-ROLLOUT.v1 | event | MODEL | DATA | active |
| DS-TRAINMIX.v1 | dataset | DATA | MODEL | active |
| EVAL-BENCH.v1 | eval | DATA | MODEL | active（approval: committee） |
| MDL-SERVE.v1 | model | MODEL | AGENT | active |
| DQ-QUALITY.v1 | metric | DATA | MODEL | active |
| TRN-HEALTH.v1 | metric | MODEL | DATA | active |
| FLY-CYCLE.v1 | metric | DATA | MODEL | active |
