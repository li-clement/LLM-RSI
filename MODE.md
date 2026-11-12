# 三平面协同模式（TriPlane）

> 版本 v0.1 · 状态：提案 · 维护者：Spec 平面委员会
>
> 一句话：**Spec 是跨部门谈判与冻结的机制，Knowledge 是可复利的组织记忆资产，Pipeline 是把执行变成可验证证据的机制。AI Agent 是三个平面上的一等工作者。**

---

## 1. 定义与出发点

多 BU / 跨部门协同的根本矛盾是：**组织是树状的，而交付依赖是网状的**。传统的解法要么靠会议缝合（慢、不可追溯），要么靠个人关系缝合（不可扩展），要么把接口写进 Word 和群聊（必然漂移）。

TriPlane 把跨边界协同的三种核心资产拆到三个独立版本化、独立治理、通过 ID 引用互相咬合的"平面"：

| 平面 | 回答的问题 | 核心工件 | 网络类比 | 详见 |
|---|---|---|---|---|
| **Spec 平面** | 我们要共同构建什么？部门边界在哪？ | Epic → Feature → Contract → Scenario | 控制面（决定意图与路由） | §3 |
| **Knowledge 平面** | 我们知道什么？为什么这样决定？ | 术语表 / 能力卡 / ADR / 模式 / 坑点 / Runbook | 管理面（配置与记忆） | §4 |
| **Execution 平面** | 事实是什么？证据在哪？ | 四条流水线 + 门禁产物 | 数据面（承载流量） | §5 |

三平面闭环：

```
        冻结意图                验证契约               沉淀经验
 Spec 平面 ────────► Execution 平面 ────────► Knowledge 平面
    ▲                      │                        │
    └───── 滋养下一轮 Spec ◄┴────── 回流（自动/复盘）─┘
```

**Agent 一等公民**意味着：三个平面的每个工件都有机器可读结构（frontmatter / x-contract / JSON Schema），Agent 直接消费它们干活（生成、校验、影响分析、测试编织），Agent 的产出也落回三个平面并带溯源。人负责**批准与冻结**，Agent 负责**起草与验证**。

---

## 2. 它治什么病（失效模式 → 对策）

| 典型病症 | 根因 | 三平面对策 |
|---|---|---|
| 集成黑洞：联调周才发现接口对不上 | 契约活在文档/聊天记录里，无人守护 | 契约是 Spec 仓库中版本化的 JSON 工件，CI 每次 PR 做兼容性 diff |
| 会议驱动进度 | 没有可异步消费的单一事实源 | 冻结点之后一切变更走 CR 流程，会议只做决策，不做同步 |
| 知识在个人头上，人走知识走 | 知识无 ID、无生命周期 | 六类知识资产有元数据、TTL、出处，过期自动降级为候选 |
| 重复造轮子、重复踩坑 | 经验不可检索、不被强制消费 | Code Review 与 Agent 执行前必须引用相关知识项 ID |
| 发布日惊喜 | 跨 BU 交付没有证据链 | 四流水线 + 五道门禁，每个门禁产出可审计证据 |
| AI Agent 输出跑偏、不可信 | 上下文是聊天记录而非结构化资产 | 三平面即 Agent 的工作记忆；Agent 产出落回平面并带 provenance |

---

## 3. Spec 平面

### 3.1 工件链

```
Epic（业务结果）
  └─ Feature Spec（一个可验收的跨部门能力，含职责切分）
       ├─ Contract（API / Event / Data，机器可读，独立版本化）
       └─ Scenario（验收场景 = 可执行测试的地基；契约场景 = 消费者期望）
```

### 3.2 状态机（Feature 与 Epic 共用）

```
draft ──► in-review ──► approved ──► frozen ──► released
                                       ▲
                          （仅 CR 流程可变更契约，frozen 后）
```

**冻结点语义**：`frozen` 之后，契约只能经 Contract Change Request（CR）修改。冻结 = 责任切换——此前讨论是成本，此后每个破坏性变更都是事故。这是跨部门问责的锚点。

### 3.3 命名与 ID

| 工件 | ID 格式 | 文件名 |
|---|---|---|
| Epic | `E-<num>` | `specs/epics/E-001-<slug>.md` |
| Feature | `F-<year>-<num>` | `specs/features/F-2026-001-<slug>.md` |
| Contract | `<域码>-<动作>.v<major>` | `specs/contracts/ORD-CREATE.v1.openapi.json` |
| Scenario | `S-<num>` | `specs/scenarios/S-001-….md` |

ID 是三个平面之间的**唯一引用货币**。任何其他位置出现某个事实（比如知识库里写"ORD-CREATE 支持幂等键"）必须引用 ID 而非复制内容（单一事实源原则）。

### 3.4 契约版本与兼容性

- 契约文件内嵌 `x-contract` 元数据（id / kind / version / status / owner / consumers / compatibility），见 [specs/contracts/README.md](specs/contracts/README.md)。
- 兼容性策略显式声明（默认 `backward`）。破坏性变更 = 新 major 版本文件 + 旧版本标记 `deprecated` + `sunset` 日期 + 迁移方案（CR 模板强制填写）。
- 每个契约必须至少有一个 `kind: contract` 的契约场景（消费者期望），否则 CI 失败——**没有消费者测试的契约不允许存在**。

---

## 4. Knowledge 平面

### 4.1 六类知识资产

| 类型 | 目录 | 回答 | 典型产生时机 | TTL |
|---|---|---|---|---|
| 术语表（domain） | `knowledge/domain/` | 这个词跨 BU 到底指什么 | S1 共创 | 90 天 |
| 能力卡（capability） | `knowledge/capabilities/` | 这个 BU 提供什么契约、边界与非目标 | 每季度 | 90 天 |
| 决策记录（ADR） | `knowledge/decisions/` | 为什么选 A 不选 B | 每次架构决策 | 无（被取代而非过期） |
| 模式（pattern） | `knowledge/patterns/` | 这类问题怎么解 | 方案设计 | 180 天 |
| 坑点（pitfall） | `knowledge/pitfalls/` | 哪里会炸、怎么探测 | 事故/联调 | 180 天 |
| Runbook | `knowledge/runbooks/` | 出事/发布时按什么步骤做 | 每次发布演练 | 90 天 |

### 4.2 元数据即生命周期

每个知识项的 frontmatter 必含：`id, type, scope, owner, confidence, provenance, expires`。规则：

- **TTL 到期自动失效**：`check.py` 会报错，条目降级为 `candidate` 直到有人复核——知识不允许"僵尸化"。
- **无消费则死亡**：90 天无任何 Spec/场景引用的知识项会被 `stats` 报告点名。写了没人用的知识是负债。
- **provenance 强制**：每个知识项必须写明出处（事故编号、MR、复盘、契约 ID）。Agent 生成的候选知识必须标注 `agent:<playbook>` + pipeline run，由 Curator 复核后发布。

### 4.3 回流机制（Execution → Knowledge）

三条自动/半自动回流通道：

1. **knowledge-distiller Agent**：每次契约 CR 批准、每次事故关闭、每次发布后，从 diff 和复盘中抽取候选知识项（见 [agents/playbooks.md](agents/playbooks.md)）。
2. **复盘门禁**：G5 门禁要求发布后观察期结束前，至少一条知识项被新建或复核（防"复盘只写在周报里"）。
3. **人工 Curator 周会**：30 分钟，只做一件事——把 `candidate` 提升为 `accepted` 或拒绝。

---

## 5. Execution 平面：四流水线 + 五门禁

| 流水线 | 触发 | 核心阶段 | Agent 嵌入点 |
|---|---|---|---|
| **P1 Spec 流水线** | Spec 仓库每个 PR | 三平面校验 → 契约 lint → 契约兼容性 diff → 影响分析摘要 | spec-summarizer, contract-impact, compat-reviewer |
| **P2 BU 开发流水线** | 各 BU 自己仓库 push | 构建/单测 → **契约消费者测试** → 知识引用门禁 | scenario-forge, test-weaver, knowledge-distiller |
| **P3 集成流水线** | 契约进入 `frozen` | 从契约自动装配虚拟化集成环境 → 跑全部 Scenario → 出证据报告 | compat-reviewer |
| **P4 发布流水线** | KB（跨 BU 联签）通过后 | 发布编排（flag/灰度/回滚点）→ 观察期 → 回流检查 | release-orchestrator |

五道跨部门门禁（详见 [pipelines/README.md](pipelines/README.md)）：

```
G1 三平面校验绿  →  G2 契约冻结    →  G3 CDC 全绿      →  G4 KB 联签      →  G5 观察期+回流完成
   (P1)              (S2 结束)         (P2/P3)             (P4 前置)          (P4 后置)
```

---

## 6. 角色与治理

角色是**帽子不是编制**，可由现有工程师兼任，但每个工件必须有人戴着对应的帽子。

| 角色 | 人数建议 | 职责 | 独占权限 |
|---|---|---|---|
| **接口委员会** | 各 BU 技术负责人 + 架构办 | 批准 CR、仲裁边界争议、月度契约健康复盘 | 批准破坏性变更 |
| **Spec Owner** | 每个 Feature 1 个 | 起草并推进 Feature 到 `frozen` | 提交冻结申请 |
| **Contract Steward** | 每个契约 1 个（提供方 BU） | 守护契约兼容性，批准 CR | 批准契约变更、执行冻结 |
| **Knowledge Curator** | 每 BU 1 个 | 候选知识复核、TTL 维护、术语仲裁 | 发布 `accepted` 知识 |
| **Delivery Steward** | 每次跨 BU 发布 1 个 | 编排 P4、主持 KB 与回滚决策 | 宣布 Go/No-Go |

决策权矩阵（谁说了算）：

| 事项 | 起草 | 审核 | 批准 |
|---|---|---|---|
| Feature Spec | 任一相关 BU | 其他 BU + Spec Owner | 接口委员会 |
| 契约兼容性变更（非破坏） | 消费方或提供方 | Contract Steward（对方） | Contract Steward |
| 契约破坏性变更 | CR 发起人 | contract-impact Agent 报告 + 双方 | 接口委员会 |
| 知识项发布 | 任何人 / Agent | — | Knowledge Curator |
| KB 发布 | Delivery Steward | 各 BU Steward | Delivery Steward（Go/No-Go） |

**Agent 权限三闸门**（不可妥协）：Agent 可以起草、验证、生成候选、开 PR；Agent **不能**批准、冻结、发布知识、执行上线。所有 Agent 产出必须带 provenance 标注，由持帽人复核。

---

## 7. 流程：五阶段生命周期

| 阶段 | 输入 | 关键活动 | 出口门禁 | 输出 |
|---|---|---|---|---|
| **S1 共创** | 业务诉求 | 跨 BU 工作坊：定 Epic/Feature、对齐 CONTEXT.md 术语 | G1 | `approved` 的 Feature |
| **S2 冻结** | Feature | 契约起草 + Scenario 三方评审 + spec-summarizer 影响分析 | **G2** | `frozen` 契约、契约场景 |
| **S3 并行开发** | 冻结的契约 | 各 BU P2 流水线开发；从契约生成 mock 虚拟化对端；Agent 结对写测试 | G3（各 BU） | 通过 CDC 的实现 |
| **S4 契约收敛** | 各方实现 | P3 集成：跑全部 Scenario；兼容性终审；坑点知识消费检查 | **G3** | 集成证据报告 |
| **S5 发布与回流** | 集成证据 | KB 联签（G4）→ P4 编排发布 → 观察期 → distiller 候选知识 → Curator 发布 | **G5** | released + 新知识项 |

异步默认：S1 允许一次工作坊，之后一切讨论附着在工件（PR 评论、CR、Scenario diff）上进行。会议只做两件事：冻结决策与仲裁争议。

---

## 8. 指标体系：度量接口稳定性，不度量工时

| 指标 | 定义 | 目标 | 采集 |
|---|---|---|---|
| 契约冻结后破坏性变更数 | G2 之后合入的 breaking diff | **0** | P1 兼容性 diff 日志 |
| CDC 覆盖率 | 有可运行契约测试的消费方 / 契约声明的 consumers | 100% | P2/P3 |
| Scenario 通过率 | P3 全量场景执行 | 100%（KB 前置） | P3 证据报告 |
| 知识新鲜度 | 未过期知识项占比 | ≥ 90% | `check.py stats` |
| 知识消费率 | 被 Spec/场景引用的知识项占比 | 持续增长 | `check.py stats` |
| Agent 产出采纳率 | Agent 草稿被直接/小改合并的比例 | 趋势上升 | PR 元数据 |
| 跨部门前置时间 | 冻结 → KB 通过 | 逐季下降 | P1–P4 时间戳 |
| 联调期缺陷数 | S3–S4 发现的跨 BU 缺陷 | 逐季下降 | 缺陷打标 |

Agent 产出采纳率是整个模式的**元指标**：它衡量的是"我们的 Spec 和知识质量高到 Agent 能直接干活吗"——这是 SDD + 知识工程是否成功的终极检验。

---

## 9. 落地路线图与反模式

### 90 天试点

| 周期 | 动作 | 验收 |
|---|---|---|
| 第 1–4 周 | 选 1 个中等疼痛、边界清晰的跨 BU 需求；建 Spec 仓库骨架（本仓库复制）；填 2 张能力卡 + 术语表；`check.py` 进 CI | G1 常绿 |
| 第 5–8 周 | 完成 1 次完整 S1→S2（真实契约冻结）；接入 1 个 BU 的 P2 契约测试；启动 Curator 周会 | 首个 G2 |
| 第 9–12 周 | 第 2 个 BU 接入；上线 3 个 Agent playbook（summarizer / test-weaver / distiller）；完成首次 KB 发布 | 首个 G4+G5 |

选试点场景的原则：**双方都有存量系统、接口数量 3–10 个、业务价值明确**。不要选全新系统（没有契约可冻结），也不要选 >20 个接口的大杂烩（治理过载）。

### 反模式自查

- **流程官僚化**：门禁超过 5 道、CR 审批超过 3 人 → 模式在腐烂，砍掉。
- **Spec 完美主义**：冻结粒度必须是接口粒度，绝不是代码行粒度。Feature spec 超过 3 页就该拆。
- **知识坟场**：知识项只写不引用 → 靠"无消费则死亡"规则强制清退。
- **假 Agent 一等公民**：只让 Agent 写代码、不让它读契约与知识 → 先让 check.py 报告成为每个 Agent 的第一上下文。
- **双事实源**：wiki/群公告里复述契约内容 → 只准引用 ID。

---

## 10. 本仓库 = 模式工具箱

```
├── MODE.md                  ← 本文：模式设计
├── AGENTS.md                ← Agent 一等公民入口（任何 Agent 进仓库先读它）
├── specs/                   ← Spec 平面：规则 + 示例工件链（Epic/Feature/Contract/Scenario）
├── knowledge/               ← Knowledge 平面：规则 + 六类示例资产
├── pipelines/               ← Execution 平面：四流水线与门禁定义 + CI 配置示例
├── agents/                  ← 7 个流水线内嵌 Agent 的 playbook
├── templates/               ← 六类工件模板，复制即用
└── tools/check.py           ← 三平面一致性校验器（CI 的守门人）
```

使用方式：① 把本骨架复制到公司级 `triplane` 仓库（一个 Spec 仓库服务所有跨 BU 项目）；② 各 BU 填能力卡与术语表；③ `tools/check.py` 挂进 Spec 仓库 CI（见 `pipelines/ci/`）；④ 按 §9 路线图试点一个真实需求；⑤ 各 BU 仓库按 `pipelines/ci/bu-dev-ci.example.yml` 接入契约测试。
