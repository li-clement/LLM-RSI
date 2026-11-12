# 指标契约模板（metric，第六类契约）

> 文件：`specs/contracts/<域码>-<主题>.v<N>.metric.json`。域码建议：`DQ` 数据开发 / `TRN` 模型训练 / `FLY` 飞轮循环。
> 纪律：**先有指标契约，后有采集实现、看板与告警**——顺序不可反。

```json
{
  "x-contract": {
    "id": "<域码>-<主题>",
    "kind": "metric",
    "version": "1.0.0",
    "status": "active",
    "owner": "<定义口径的团队>",
    "consumers": ["<读这些数字做决策的团队>"],
    "compatibility": "backward",
    "steward": "@<指标契约负责人>"
  },
  "x-telemetry": {
    "collect": "<在哪个流水线阶段、由哪个组件上报、快照落哪个 reports/ 路径>",
    "metrics": [
      {
        "id": "<snake_case 指标 ID，全局唯一>",
        "def": "<口径：一句话可执行定义，含窗口与聚合>",
        "unit": "ratio | count | days | tokens | CNY | percentage-point ...",
        "slo": "<可判定表达式，如 >= 0.99 / == 0 / <= 7>",
        "alert": "warn@<值> crit@<值>（可选；crit 必须挂门禁或路由）",
        "binds": "<可选：绑定到 dataset/eval 契约的同一断言——搬运原值，禁止二次实现>",
        "informational": true,
        "note": "<为什么存在 / 怎么消费>"
      }
    ]
  },
  "title": "<指标主题契约>",
  "description": "<口径变更走 CR；SLO 收紧算非破坏，放宽算破坏；删除指标 = 破坏性>"
}
```

## check.py 会强制的事

- 每个指标条目必须有 `id/def/unit`；且**要么有 `slo`，要么标 `informational: true`**（没有阈值的指标只是数字）；
- 指标 ID 全局唯一（跨契约不重复定义——单一事实源）；
- `x-telemetry.collect` 必填（口径必须绑定发射点）；
- 所有 `observability/dashboards/*.board.json` 面板引用的 metric 必须存在于契约注册表（裸名禁止）。

## 调优路由提醒

改 `slo`/`def` 前想清楚粒度：参数级（实现里调，登记指纹）/ 口径级（本契约 CR）/ 尺子级（只有 `EVAL-*` 走委员会）。指标契约本身不是裁判——**裁判定义在 eval 契约里**，metric 契约是体检仪表。
