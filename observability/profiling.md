# Profiling 与调优工作流

> 调优不是"看着仪表盘随手改"，而是**有节奏、有指纹、有回流**的循环。三层 profiling 对应三种调优粒度。

## 三层节奏

### 1. 批级（batch-level）——每个数据批次，自动

- **内容**：分布漂移（PSI/KL 对比上一批次）、空值/去重/线绪完备率、mix 构成、token 长度分桶、与 holdout 相似度分（预检）。
- **产物**：`reports/<batch>/profile.json`（全部用 DQ-QUALITY 指标 ID）。
- **调优粒度**：清洗规则、过滤阈值、采样配比建议——**参数级自由**，但改动要登记进批次 manifest（前后指标差值对比可见）。
- **红线**：改 `source` 定义、deny-list 逻辑 = 口径级 → CR（Dataset Steward）。

### 2. run 级（training-level）——每个训练 run，自动

- **内容**：算力侧（MFU、tokens/hr、通信占比、重启损耗）、优化侧（loss spike、grad norm、KL 漂移）、样本侧（reward 分布、judge 分歧率、hacking 探测标记）。
- **工具占位**：torch.profiler / Nsight、TensorBoard/W&B 类实验跟踪——但**指标名一律映射到 TRN-HEALTH ID**，实验系统只是渲染器。
- **调优粒度**：超参、并行策略、数据加载管线——自由，**前提是 run 登记实验指纹**（数据集版本 + EVAL 协议版本 + 配置哈希，`trn_fingerprint_reg_rate == 1.0`）。没指纹的调优结果不可比，G3 拒收。
- **红线**：judge/评测 proxy 换版 = 尺子级 → 委员会。

### 3. 循环级（cycle-level）——每轮 S5 收口，Release Steward 主持

- **内容**：flywheel.json 快照（FLY-CYCLE 指标全量重算）、成本曲线、断点分析（哪一段等待最久：回流？审计？灰度观察？）。
- **调优粒度**：循环结构——批次 cadence、审计通道并行化、灰度阶梯时长。**这类调优改的是流水线不是模型**，走 Spec 平面（新 Feature 或 CR）。
- **下一步输入**：下一轮 S1 立靶**必须引用**上一轮 flywheel.json——目标维度从数据来，不从会议室来。

## 调优提案的分类路由（三闸门在观测域的形态）

| 提案类型 | 例子 | 路由 | 验证方式 |
|---|---|---|---|
| 参数级 | 去重相似度阈值 0.85→0.9；学习率调度 | 直接改，登记指纹 | A/B 或历史回放对比 profile.json |
| 口径级 | mix `distilled` 定义收紧；MFU 计算口径 | CR（对应 Steward） | 契约场景 diff + 影响分析 |
| 尺子级 | EVAL 指标阈值、judge_version | 委员会（RES-） | 历史 run 重评（可比性恢复证明） |

## 异常 → 知识的自动通道

- crit 告警与 `slo` 违例事件自动创建候选知识项（experiment-distiller，`provenance: alert:<rule>@<run>`）；
- 同一指标连续两周期违例 → 自动升级为 pitfall 候选（重复踩坑的机器形态）；
- 调优前后对比（profile diff）自动附在 CR §4，替代"我觉得变好了"。

## 反模式

- **仪表盘考古**：建了没人看的面板——`stats` 面板引用率月度盘点，没人消费的面板删（与知识"无消费则点名"同构）。
- **裸名指标**：报告里写"dedup 0.99"不引用 `dq_dedup_rate`——不同实现口径漂移后无法对账。
- **双实现**：监控里重新计算审计指标（不搬运原始输出）——必然漂移，S-006 #2 禁止。
- **调优不留指纹**：结果不可比，等于没调。
