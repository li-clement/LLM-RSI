# Observability 子系统：Execution 平面的神经系统

> 定位：监控与 profiling **不是第四个平面**，而是 Execution 平面的神经系统——它消费 Spec 平面定义的指标契约（第六类契约 `metric`），产出 Execution 平面的证据（profile 快照、门禁读数），并把异常回流到 Knowledge 平面。

## 五条设计原则

1. **指标即契约**（SDD 在观测域的延伸）：所有监控指标先在 `specs/contracts/*.metric.json` 定义（ID / 口径 / 单位 / SLO / 告警路由 / 采集点），再谈实现。看板、告警、报告只准引用指标 ID——**裸名指标禁止**（check.py 强制）。
2. **Dashboard-as-code**：仪表盘是指标契约的投影（[dashboards/](dashboards/) 的 `*.board.json`），面板与契约不一致 CI 即红；换可视化工具（Grafana/Superset/内部平台）只换渲染层。
3. **告警 = 门禁信号**：SLO 违例不只是通知，而是直接进入 G3/G5 证据与熔断（如 `dq_eval_leak_count > 0` 阻断本轮循环）；告警路由来自能力卡 contact。
4. **Profile 快照是证据**：批级 / run 级 / 循环级三层快照落 `reports/`，保留 ≥90 天，是 experiment-distiller 与下一轮 S1 立靶的法定输入。
5. **调优走三闸门**：参数级调优自由但必须登记实验指纹；**口径级**（SLO、mix 定义）走 CR；**尺子级**（评测指标阈值）只有委员会——与契约变更同一套权限模型。

## 场景化监控地图（六条 metric 契约）

| 生命周期位置 | 指标契约 | 覆盖 | 主要消费方 |
|---|---|---|---|
| 数据开发（采集→语料→样本） | [DQ-QUALITY.v1](../specs/contracts/DQ-QUALITY.v1.metric.json) | 作业成功率、新鲜度、体量、去重搬运、污染搬运、PII/consent、lineage、schema 漂移 | MODEL（训练决策）、G3 |
| 预训练 | [PRE-HEALTH.v1](../specs/contracts/PRE-HEALTH.v1.metric.json) | loss 异常、MFU、**位置回放完整性**、curriculum 遵守、tokenizer 指纹、重启损耗 | DATA、RB-002 |
| 中训练 | [MID-HEALTH.v1](../specs/contracts/MID-HEALTH.v1.metric.json) | needle 分桶召回、长度课程、位置方案登记、短 ctx 保持、annealing 占比对账 | DATA、G3 |
| 后训练 / RL / 对齐 | [TRN-HEALTH.v1](../specs/contracts/TRN-HEALTH.v1.metric.json) | KL 漂移、verifier 分歧、advantage 塌缩、reward hacking 探测、实验指纹完备率 | DATA（评测排期）、G3 |
| RAG 在线 | [RAG-HEALTH.v1](../specs/contracts/RAG-HEALTH.v1.metric.json) | 命中率、引用新鲜/有效、**版本歪斜探针**、缺口信号（喂飞轮） | DATA 语料管道、G5 |
| 数据飞轮（循环级） | [FLY-CYCLE.v1](../specs/contracts/FLY-CYCLE.v1.metric.json) | 回流转化率、前置时间、净增益、污染事件、换尺子观测、负结果处置数 | 下一轮 S1、治理委员会 |

## 遥测管道

```
P2/P3 阶段 hooks ──► metrics-store（TSDB 占位：Prometheus/ClickHouse 类）
        │                     │
        └─► reports/<run>/    ├──► board 渲染（dashboards/*.board.json → Grafana 类）
            profile.json      └──► 告警引擎（slo + alert 字段直译）
                    │
                    └──► experiment-distiller / flywheel.json → 下一轮循环 S1
```

采集实现放各团队仓库（`quality_suite`、`trainkit` hooks），Spec 仓库只存定义与仪表盘规格——防止"监控配置四处漂移"。

## 与 check.py / stats 的关系

- `check.py` 校验：指标条目必须有 `slo` 或 `informational: true`；`binds` 指标不得二次实现（场景断言）；board 面板引用的 metric 必须存在于契约注册表；指标 ID 跨契约唯一。
- `check.py stats` 输出指标契约总数与仪表盘引用健康度——G1 的一部分。

## 目录

```
observability/
├── README.md          ← 本文
├── profiling.md       ← 批级/run 级/循环级节奏 + 阶段专属调优手感的落点
└── dashboards/
    ├── rsi-flywheel.board.json      ← 主盘：数据开发/训练/RAG 在线/飞轮 + 告警联动
    └── training-stages.board.json   ← 训练阶段盘：预训练/中训练/后训练三段
```
