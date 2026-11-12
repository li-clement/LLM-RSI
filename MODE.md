# 三平面协同模式（TriPlane）· RSI 适配版

> 版本 v0.2 · 状态：提案 · 维护者：RSI 治理委员会
> 适用背景：**跨数据团队（DATA）与模型团队（MODEL）的递归自我改进（Recursive Self-Improvement）项目**，下游由 Agent 平台团队（AGENT）消费模型服务。
>
> 一句话：**Spec 是跨团队谈判与冻结的机制，Knowledge 是可复利的研究记忆，Pipeline 是把"这一轮真的变好了"变成可审计证据的机制。AI Agent——包括 RSI 循环自身产生的改进提案——是三平面上受三闸门约束的一等工作者。**

---

## 1. 定义与出发点

RSI 项目的协同矛盾比普通跨部门更尖锐：**递归循环的每个环节都横跨团队边界**——模型团队产出轨迹，数据团队清洗组装成训练集，评测决定"是否更好"，再回到模型团队发布新 champion。任何一处边界靠口头默契，整个循环就会在"到底有没有变好"上失焦，甚至退化为**自说自话的自我表扬**。

TriPlane 把协同的三种核心资产拆到三个独立版本化、通过 ID 引用咬合的平面：

| 平面 | 回答的问题 | 核心工件 | RSI 里的对应物 |
|---|---|---|---|
| **Spec 平面** | 这一轮改进要共同交付什么？边界在哪？ | Epic → Feature（循环规格）→ Contract → Scenario | 数据集契约、轨迹事件契约、评测协议契约、模型服务契约 |
| **Knowledge 平面** | 我们知道什么？哪些路试过不通？ | 术语表 / 能力卡 / ADR / 模式 / 坑点 / Runbook | 失败案例、mix 配比经验、判分口径裁定、实验结论 |
| **Execution 平面** | "变好了"的证据在哪？ | 四流水线 + 五门禁 | 污染审计、评测复现、数据质量断言、champion/challenger 灰度 |

三平面闭环与 RSI 循环天然同构：

```
      冻结本轮契约              执行循环 + 评测取证          蒸馏实验经验
Spec 平面 ────────► Execution 平面 ────────► Knowledge 平面
    ▲                    │                        │
    └── 下一轮循环的 spec ◄┴──── 回流（自动/复盘）──┘
```

**Agent 一等公民 + RSI 自提案治理**：改进循环自身会生成提案（模型建议的新数据 mix、训练配置、prompt 补丁、契约变更草稿）。本模式把它们与流水线 Agent 同等对待——**可以起草、可以验证，不得批准**。递归被允许，**换尺子不被允许**。

---

## 2. 它治什么病（失效模式 → 对策）

| 典型病症 | 根因 | 三平面对策 |
|---|---|---|
| 自说自话：模型团队自评自夸，数据团队不知情 | 评测权与训练权不分离 | **三权分立**：训练权（MODEL）、评测权（DATA）、阈值冻结权（治理委员会），见 ADR-0001 |
| 换尺子：指标口径悄悄漂移，"提升"不可比 | 评测协议活在脚本和口头里 | 评测协议是 `EVAL-BENCH` 契约；**改阈值/口径一律视为破坏性变更，只有委员会可批** |
| 评测污染：holdout 混进训练 mix（含蒸馏/合成衍生） | 训练侧与评测侧数据无隔离审计 | 污染审计是 P3 硬门禁；泄漏计数 = 0 是数据集契约的质量断言 |
| 数据契约漂移：训练集 schema/口径变更打挂下游 | 数据集版本活在文件名里 | 数据集契约版本化 + schema-diff CI + 契约场景（S-xxx） |
| "这轮到底好在哪"说不清 | 循环没有 spec，只有实验日志 | 每轮 = 一个 Feature（循环规格）：目标维度、回归地板、预算，frozen 后才开跑 |
| 知识在研究员个人头上、负结果被遗忘 | 实验结论无 ID、无 TTL、无消费责任 | 知识六类资产 + 无消费则点名 + experiment-distiller 自动回流候选 |
| 发布日惊喜：新模型上线打挂线上 | 无灰度/回滚证据链 | champion–challenger 模式（PAT-001）+ P4 编排 + G5 观察期 |

---

## 3. Spec 平面

### 3.1 工件链

```
Epic（改进方向，如"工具调用能力闭环"）
  └─ Feature = 循环规格（一个可验收的改进循环：目标维度 / 回归地板 / 预算 / 职责切分）
       ├─ Contract（五类，机器可读 JSON，独立版本化）
       └─ Scenario（acceptance 端到端验收 / contract 契约断言）
```

### 3.2 五类契约

| kind | flavor | 承载 | 必填扩展（check.py 强制） |
|---|---|---|---|
| `dataset` | `.schema.json` | 训练/评测数据集：记录 schema + SLA + 质量断言 | `x-sla`（cadence、freshness、min_count）、`x-quality`（≥1 条可执行断言，含污染审计） |
| `event` | `.asyncapi.json` | 轨迹回流流：rollout 事件的投递契约 | 标准 asyncapi 本体 |
| `api` | `.openapi.json` | 同步服务接口（如有） | 标准 openapi 本体 |
| `eval` | `.eval.json` | **评测协议**：基准、指标定义、阈值、隔离规则 | `x-protocol`（benchmark / metrics / thresholds / isolation）+ `x-contract.approval: committee` |
| `model` | `.model.json` | 模型服务契约：接口签名、预算、降级、已知失效清单 | `x-signature`、`x-budget`、`x-fallback` |

### 3.3 状态机与冻结点

```
draft ──► in-review ──► approved ──► frozen ──► released
                                        ▲
                       （frozen 后只能走 CR；eval 契约任何实质变更必须委员会）
```

**冻结点语义（RSI 版）**：Feature 进入 `frozen` = 本轮循环开跑的起跑线——数据 mix 口径、评测协议、模型接口在此刻锁定。此后"这轮有没有变好"只对 frozen 版本负责；任何中途换尺子、换 mix 都是事故或新一轮循环。**循环进行中禁止修改 frozen 契约——这是可比性的来源。**

### 3.4 命名与版本

ID 规则见 [specs/README.md](specs/README.md)；域码表：`TRJ`（轨迹，MODEL 域）、`DS`（数据集，DATA 域）、`EVAL`（评测协议，DATA 域）、`MDL`（模型服务，MODEL 域）。

- 非破坏变更：schema 加可选字段、SLA 收紧 → minor。
- 破坏性变更：字段删除/枚举收窄/必填新增/mix 口径变更 → 新 major + 旧契约 `sunset` 双跑；**评测协议的任何阈值与指标定义变更，无论 schema 上是否"兼容"，一律按破坏性处理**。
- 每个契约必须 ≥1 个契约场景，否则 G1 失败——**没有断言的数据集不是资产，是负债**。

---

## 4. Knowledge 平面

六类资产（术语表 / 能力卡 / ADR / 模式 / 坑点 / Runbook）与生命周期规则（ID、TTL、出处、无消费则点名）见 [knowledge/README.md](knowledge/README.md)，与 v0.1 相同。RSI 语境下的重点：

- **负结果是一等知识**：失败的训练配方、无效的 mix、打挂评测的补丁——pitfall 类是 RSI 项目最值钱的资产，防止循环烧算力重走死路。
- **实验结论必须落 ID**：每轮循环结束，run 报告的关键结论由 experiment-distiller 生成候选知识项；Curator 周会只处置候选，不写周报坟场。
- **口径词进术语表**：什么叫"成功"、什么叫"回归维度"、judge 版本口径——`CONTEXT.md` 是唯一仲裁源；评测指标的语义挂在 `EVAL-BENCH` 契约里，术语表只裁定概念，不复述定义。
- **单一事实源**：数据字段、阈值、接口签名只引用契约 ID；知识项里复述 = 评审打回。

回流三通道：distiller（CR 关闭 / 事故复盘 / **循环 run 结束**触发）、G5 回流门禁（每轮至少处置 1 条候选知识）、Curator 周会。

---

## 5. Execution 平面：四流水线 + 五门禁

| 流水线 | 触发 | 核心阶段 | Agent 嵌入点 |
|---|---|---|---|
| **P1 Spec 流水线** | Spec 仓库 PR | `check.py --strict` → schema-diff（数据集/接口兼容性）→ **eval 协议 diff（任何阈值变化自动标红）** → 影响分析 | cycle-summarizer, contract-impact, compat-reviewer |
| **P2 团队开发流水线** | DATA 数据管道 / MODEL 训练管道 push | 数据侧：质量断言即测试（S-003 直译）；模型侧：训练配置必须引用 frozen 契约版本 + **污染预检** | assertion-forge, test-weaver |
| **P3 收敛流水线（评测）** | 契约进入 `frozen` | 装配 frozen 环境 → 污染审计（holdout ∩ 训练 mix = ∅）→ 评测套件双跑（复现偏差 ≤ ε）→ 数据质量断言全绿 → 证据报告 | compat-reviewer |
| **P4 发布流水线** | KB 联签后 | champion–challenger 编排：shadow 双跑 → 灰度 1%→10%→100% → 熔断探针（直接用契约断言）→ 观察期 → 回流 | release-orchestrator, experiment-distiller |

五道门禁：

```
G1 三平面校验绿   → G2 契约冻结      → G3 收敛全绿            → G4 KB 联签   → G5 观察期+回流完成
   (P1)              (循环起跑线)       (污染=0·评测复现·断言100%)   (上线联签)      (champion 转正)
```

**G3 是 RSI 的生命线**：三条硬条件——① 污染审计泄漏计数 = 0；② 评测双跑复现偏差 ≤ 阈值（可复现才可比）；③ 全部契约场景 + 验收场景 100% 通过。任一不满足，本轮循环记为"未完成"，challenger 不得进 KB。

---

## 6. 角色与治理（三权分立）

角色是帽子不是编制；每个工件必须有人戴着对应的帽子。

| 角色 | 归属 | 职责 | 独占权限 |
|---|---|---|---|
| **RSI 治理委员会** | DATA+MODEL 负责人 + 架构办 | 冻结评测阈值口径、仲裁"变好了吗"争议、批准破坏性 CR | 批准 eval 契约变更 |
| **Cycle Owner**（原 Spec Owner） | 每轮循环 1 个（两团队轮值） | 起草循环规格、推进到 frozen | 提交冻结申请 |
| **Dataset Steward** | DATA | 守护数据集契约与 SLA | 批准 dataset 契约 CR |
| **Eval Steward** | DATA | 守护评测协议与隔离规则 | 执行评测、拒绝私下评测请求 |
| **Model Steward** | MODEL | 守护模型服务契约与注册表 | 批准 model/event 契约 CR |
| **Knowledge Curator** | 每团队 1 个 | 候选知识（含负结果）复核发布 | 发布 `accepted` |
| **Release Steward**（原 Delivery Steward） | 每次发布 1 个 | 编排 P4、主持 KB 与熔断 | Go/No-Go |

关键结构：**训练权、评测权、阈值冻结权三分立**。MODEL 团队可以提议改指标（CR），不能改（委员会权限）；DATA 团队执行评测但不能降阈值（评测权对委员会透明）。这是防 Goodhart 化（指标被优化到失真）的组织学防线。

**Agent 与自提案三闸门**（不可妥协）：流水线 Agent 与 RSI 循环自身产生的提案（模型生成的 mix 建议、训练补丁、接口变更草稿）一律：可以起草、验证、开 draft PR；**不得批准、不得冻结、不得改 eval 协议、不得执行上线**。所有自提案必须带 `provenance: agent:<playbook>@<run>` 或 `provenance: model:<version>@<episode>`，由持帽人处置。

---

## 7. 流程：一个改进循环的五阶段

| 阶段 | 输入 | 关键活动 | 出口门禁 | 输出 |
|---|---|---|---|---|
| **S1 立靶** | 上轮证据 + 知识库 | 定本轮目标维度、回归地板、预算；对齐术语 | G1 | `approved` 循环规格 |
| **S2 冻结** | 循环规格 | 四个契约冻结：mix 口径、评测协议版本、模型接口、轨迹 schema | **G2** | 起跑线锁定 |
| **S3 造轮子** | frozen 契约 | 并行：轨迹采集清洗（DATA）+ 训练 challenger（MODEL）；消费上轮 pitfall 防重走死路 | 各团队 G3 子项 | challenger + 训练集版本 |
| **S4 收敛评审** | challenger | P3：污染审计 → 评测双跑 → 回归矩阵；失败也要出完整证据 | **G3** | 证据报告 |
| **S5 转正与回流** | 证据 | KB 联签 → champion–challenger 灰度 → 熔断观察 → distiller 蒸馏本轮（含负结果）→ Curator 处置 | **G5** | 新 champion + 知识 + 下一轮候选目标 |

注意 **S4 失败也是产出**：challenger 没赢过 champion，G3 证据同样归档，且"为什么没赢"必须成候选知识——RSI 的"递归"不只发生在成功路径上。

异步默认：一切讨论附着在工件上（PR 评论、CR、契约 diff、评测报告）。会议只做两件事：S2 冻结决策与 G4 联签。

---

## 8. 指标体系：度量循环的可信度，不度量算力

| 指标 | 定义 | 目标 | 采集 |
|---|---|---|---|
| 污染事故数 | G2 后发现的训练–评测泄漏 | **0** | P3 审计日志 |
| 换尺子次数 | 未经委员会的指标/阈值变更 | **0** | P1 eval diff 标红记录 |
| 回归维度违规数 | 每轮 champion 转正时 guard 维度下降 >0.5% 的个数 | **0** | P3 回归矩阵 |
| G3 通过率 | 收敛全绿的循环占比 | 趋势↑（失败循环也要有证据） | P3 报告 |
| 数据契约 SLA 达标率 | 新鲜度/体量/质量断言通过率 | ≥99% | P2 质量断言 |
| 评测复现偏差 | 双跑差值 | ≤ 0.3pp | P3 |
| 循环前置时间 | G2 → 新 champion 转正 | 逐季下降 | P1–P4 时间戳 |
| 知识新鲜度 / 消费率 / Agent 与自提案采纳率 | 同 v0.1 定义 | ≥90% / ↑ / ↑ | `check.py stats` + PR 元数据 |

**采纳率与"换尺子次数"是元指标对**：前者衡量平面质量，后者衡量治理硬度。自提案采纳率上升 + 换尺子恒为 0，才说明 RSI 在受控递归。

---

## 9. 落地路线图与反模式

### 90 天试点（以本项目 RSI 循环为载体）

| 周期 | 动作 | 验收 |
|---|---|---|
| 第 1–4 周 | 建 Spec 仓库骨架（本仓库）；DATA/MODEL 填能力卡与术语表；把**现有**评测脚本的口径誊成 `EVAL-BENCH.v1` 草案；`check.py` 进 CI | G1 常绿 |
| 第 5–8 周 | 跑通第一个完整循环：1 个 Feature frozen → 轨迹契约 + 训练集契约上 P2 断言 → P3 污染审计 + 评测双跑出证据 | 首个 G2+G3 |
| 第 9–12 周 | 第 1 次 champion–challenger 灰度 + KB；上线 3 个 playbook（cycle-summarizer / assertion-forge / experiment-distiller）；Curator 周会开始处置候选 | 首个 G4+G5 |

试点选靶原则：**选一个可自动判分的窄能力维度**（如工具调用成功率），guard 维度取 2–3 个全局指标。不要第一轮就改通用能力（评测不可信 = 一切归零）。

### 反模式自查

- **换尺子**：绕过委员会调阈值 → G1 自动标红 + 治理红线。
- **自说自话**：MODEL 建"私下评测集" → Eval Steward 拒绝 + ADR-0001。
- **污染换分**：把评测题蒸馏进训练 mix → P3 审计阻断；这是 RSI 特有形态，比普通泄漏更隐蔽。
- **Spec 完美主义**：循环规格冻结在**口径与边界**粒度，不是超参粒度（超参随便调，口径不许动）。
- **负结果坟场**：失败的 challenger 只留在实验系统 → G5 回流强制蒸馏进知识平面。

---

## 10. 本仓库 = 模式工具箱（RSI 适配）

```
├── MODE.md                  ← 本文
├── AGENTS.md                ← Agent/自提案一等公民入口与三闸门
├── specs/                   ← Spec 平面：五类契约规则 + RSI 循环示例链
├── knowledge/               ← Knowledge 平面：六类资产 + DATA/MODEL/AGENT 能力卡
├── pipelines/               ← Execution 平面：四流水线（含 P3 评测收敛）+ CI 示例
├── agents/                  ← 7 个 playbook（含 experiment-distiller 实验回流）
├── templates/               ← 六类工件模板
└── tools/check.py           ← 三平面一致性校验器（G1，纯 stdlib）
```

示例链是本项目的一个真实形态循环：[E-001 RSI 最小改进循环](specs/epics/E-001-rsi-minimum-loop.md) → [F-2026-001 一个完整改进循环](specs/features/F-2026-001-one-improvement-cycle.md) → 四契约（[TRJ-ROLLOUT](specs/contracts/TRJ-ROLLOUT.v1.asyncapi.json) / [DS-TRAINMIX](specs/contracts/DS-TRAINMIX.v1.schema.json) / [EVAL-BENCH](specs/contracts/EVAL-BENCH.v1.eval.json) / [MDL-SERVE](specs/contracts/MDL-SERVE.v1.model.json)）→ 五场景 → [ADR-0001 三权分立](knowledge/decisions/ADR-0001-eval-authority-separation.md) 等知识闭环。
