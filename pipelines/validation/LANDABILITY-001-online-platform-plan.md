---
id: LANDABILITY-001
type: report
title: 无自有服务器时，用在线训推平台快速验证 RSI 可落地性（5 天 / 千元内）
status: draft
owner: "@rsi-pm（循环治理轮值）"
refs:
  - E-001
  - F-2026-001
  - S-001
  - S-004
  - S-005
  - EVAL-BENCH.v1
  - POST-EVAL.v1
  - RL-VERIFIER.v1
  - SFT-PAIRS.v1
  - MDL-CKPT.v1
  - MDL-SERVE.v1
  - FLY-CYCLE.v1
  - TRN-HEALTH.v1
  - ADR-0001
  - ADR-0002
  - PAT-001
  - PIT-001
  - PIT-002
  - RB-001
  - RB-002
  - CARD-001
  - CARD-002
  - CARD-003
provenance: agent:landability-plan@local
---

# 无自有服务器时，用在线训推平台快速验证 RSI 可落地性

> 被分析工件：`E-001` / `F-2026-001` / `S-001` / `S-004`。本文只引用契约与指标 ID，
> 不复述字段与阈值（阈值以 `EVAL-BENCH.v1.eval.json` 为唯一事实源）。

## 0. 一句话结论

**这套 RSI 的可落地性不在算力上，在"尺子是否拿得住"。** G1（三平面校验）、G2（冻结）、
G3（污染/复现/场景）这三道门禁里，真正会被"没有服务器"卡住的只有 G3 的一半和 P4 的灰度能力；
其余全部可以在 GitHub Actions + 一台按小时计费的单卡 + 一个 OpenAI 兼容网关上跑完。
**5 天、1000 元以内**可以拿到一份"能开循环 / 不能开循环"的判决，而且这个判决本身就是知识平面的一等产出。

判据不是"跑通了模型"，而是：**同一份证据交出去，别人能不能重算出同一个结论。**

## 1. 把"可落地性"拆成 7 个可证伪假设

模糊的"能不能落地"无法验证，拆成断言才能。按翻车概率排序：

| # | 假设 | 翻车概率 | 探测动作（最小成本） | 若判红怎么办 |
|---|---|---|---|---|
| H1 | 评测**可复现**：`reproducibility_gap` 达标（阈值见 EVAL-BENCH.x-protocol） | **高**（异构/共享 GPU + 连续批处理 + 非确定性解码，同一模型两次跑差 1–3pp 很常见） | 同一 champion 连跑 3 次；再各跑一次 温度=0/并发=1 与 温度=0/并发=16；对比极差 | 先把解码与判分口径钉死（温度、seed、max_tokens、并发、judge_version、分词器版本）再谈循环；若仍不可达 → 提 CR 请委员会裁（**换尺子不可自行改**，ADR-0001） |
| H2 | 污染**可审计且能隔离**：`eval_leak_count == 0` 可被机器执行 | 中（租来的训练机默认能看见你上传的一切） | 在 CPU 上跑 n-gram(MinHash) + embedding ANN 双通道，holdout 800 题 vs 训练集；实测耗时与误报 | 只下发**哈希/签名/向量**、不下发 holdout 原文；训练侧预检为本地通道，P3 为终裁（对齐 `pipelines/README.md` 污染审计口径） |
| H3 | **增益可达**：`fly_target_gain_pp` 能达标且 `fly_regression_dims == 0` | 中（多半是选错子集，不是模式失灵） | 先做"天花板实验"：用最强可用 API 在同一 holdout 上跑一遍。天花板 − champion < 3pp → 该子集没有 headroom，换子集（建议多轮工具调用深度 ≥4 段） | 换目标子集，或换目标维度；两轮仍无增益 → 记负结果入库（G5），不改阈值 |
| H4 | **成本可比**：`fly_cost_per_solve` 与 champion 同口径可测 | 中（租 GPU 按小时计费 ≠ 按 token 计费，两个端点天然不可比） | champion 与 challenger **部署在同一供给形态**（同一托管 API 平台 / 同一台机器上的两个 vLLM 实例），按 token 记账后折算 | 写清折算公式进证据报告；否则成本维度只能标 `informational`（FLY-CYCLE 已支持） |
| H5 | **灰度与秒级回滚**：RB-001 的 60 秒切回能真做 | 中高（多数平台不支持双版本并存 + 按比例分流） | 网关层双 upstream（权重路由）+ 一个 flip 脚本，实测 P95 切换耗时；再验冷启动是否打穿 `MDL-SERVE.x-budget.p99_latency_ms` | 把"平台前提"写进 RB-001（runbook 是可改的），或在网关层自建分流，不在平台上赌 |
| H6 | **门禁与自提案通道是活的** | 低 | P1 跑 `check.py --strict`；故意提一个改 EVAL-BENCH 阈值、标题不带 `CR-` 的 PR，看是否标红点名委员会决议号；`self-proposal-inbox` 走一次 draft CR | 门禁没拦住 = 模式没落地，先修门禁再谈模型（这是最便宜的一条，别跳过） |
| H7 | **数据可出域**：`consent_scope` 与平台条款相容 | 低–中（取决于你们数据来源） | 把 `SRC-INGEST.v1` 的授权范围枚举对着平台条款逐条映射；确认 holdout 与线上轨迹能否上传 | 决定形态：全托管 API（最省）还是自有云小实例（合规优先）。答案会改写 §3 的选型 |

> 顺序很重要：**H6 → H2 → H1 → H3 → H4 → H5 → H7**。前两条零成本，且能立刻淘汰"看起来能跑"的假方案。

## 2. 五天日程（每一步都有产物和门禁）

| 日 | 动作 | 产物 | 成本 | 对应门禁 |
|---|---|---|---|---|
| **D0（半天）** | 干跑门禁：`g3_dryrun.py` 用合成证据把 G3 判定跑穿；再提一个"故意违规"的 PR 验 P1 | `reports/DRY-001/g3.json` + CI 红灯截图 | ¥0 | G1 / H6 |
| **D1** | 立靶：把现有评测脚本誊成 `EVAL-BENCH.v1` 草案（800 题 holdout、3 个 guard 维度各 150–200 题、judge 版本 pin）；确认 holdout 不上训练机 | 评测协议草案 + 污染 deny-list（DATA 侧） | ¥0 | S-004 / H2 |
| **D2** | 复现性实验：champion 单卡 vLLM 或托管 API，跑 3 次 + 两种并发；算极差 | `reports/RUN-REPRO/g3.json` | ¥10–50 | G3 前哨 / H1 |
| **D3** | 采轨迹 + 组装：用 champion 在训练集同分布任务上跑 rollout，2–5k 条过 `SFT-PAIRS.v1` 断言（去重率/合成占比/lineage/泄漏=0） | 一个数据集版本 + 批级 profile 快照 + `DQ-QUALITY` 上报 | ¥20–80 | S-011 / PIT-001 |
| **D4** | challenger 训练：7B 级 QLoRA/LoRA（单卡 2–4h），注册 `MDL-CKPT.v1`（含 fingerprint 与消费位置） | ckpt + 注册记录 + `TRN-HEALTH` 快照 | ¥50–200 | S-017 / PAT-003 |
| **D5** | 双跑评测 + 灰度演练：G3 六行判定；网关双 upstream 做 10% 分流与 60 秒切回实测 | `reports/<run>/g3.json` + 切换耗时记录 | ¥30–100 | G3 / G4 前置 / H5 |
| **D6（半天）** | 收口：判决书写成报告；失败项开 `status: candidate` 知识（provenance 到 run）；需要改的口径开 **draft CR** | 判决 + 候选知识 + draft CR | ¥0 | G5 干跑 |

**总计：5.5 个工作日，GPU 支出通常落在 ¥100–400，加上对象存储与网关实例不超过 ¥1000。**
单轮 `fly_cycle_lead_time_days` 会被压到 5 天以内，远低于 21 天上限——这是"能落地"的第一个正面信号。

## 3. 平台选型：按角色分工，不要找一个"全能平台"

| 角色 | 首选（无自有服务器） | 备选 | 必须验的能力 |
|---|---|---|---|
| Spec 平面 CI（P1） | GitHub Actions（私有仓免费额度够跑 `check.py` + JSON Schema diff） | Gitee Go / 自建 runner | 能对 `specs/**` 与 `knowledge/**` 触发；能挂 `--strict` |
| 训练（P2-MODEL） | 单卡按小时实例（AutoDL / 阿里云 PAI-DSW / RunPod 一类） | 云厂商抢占式实例 | 能装 vLLM/peft；能挂载对象存储；**能证明 holdout 不在挂载盘上** |
| 推理托管（MDL-SERVE 实现） | 同机 vLLM（OpenAI 兼容 `/chat/completions`，正好对上 `MDL-SERVE.x-signature`） | 托管 API（SiliconFlow / 百炼 / OpenRouter 等） | 响应能回传 `model_version`；warm 与 cold 的 p99 分开测 |
| champion–challenger 分流与秒级回滚 | 网关层双 upstream：LiteLLM Proxy（OpenAI 兼容、支持权重路由与 fallback）或 Envoy/nginx | Cloudflare Worker 转发 | 权重可改、切换有日志、切换耗时可测量（H5 的实体） |
| 实验跟踪与注册 | MLflow（SQLite + 对象存储）或实验平台的 run 记录 | W&B 免费档 | run_id ↔ 契约版本指纹 ↔ ckpt fingerprint 可互查 |
| 产物归档 | 对象存储（OSS/S3/R2），`reports/<run>/` 原样上传 | Git LFS（不推荐，证据会膨胀） | ≥90 天可读（对齐 profile 快照留存口径） |

三条硬约束，选平台时先问清楚：

1. **holdout 原文永不进训练机**（H2）。线上平台默认"上传即可见"，所以隔离要在流程上做，不是在平台配置里做。
2. **判分器必须 pin 版本**（`judge_version`）。用托管 API 当 judge 时，厂商静默升级模型 = 换尺子（ADR-0001 明令禁止）。
3. **别用平台自带的 eval/leaderboard 当 `EVAL-BENCH` 的执行体**。平台的排名字段是它的口径，不是你的裁判（ADR-0002：四把尺子都由委员会管）。

## 4. 证据落盘形状（先定形状，再买算力）

P3 的产物形状现在是可执行的——`pipelines/validation/g3_dryrun.py` 已把校验器做出来了，阈值从契约读，不在代码里写死：

```bash
# 机制演练（合成证据，默认拒绝判绿，防止假证据混入）
python3 pipelines/validation/g3_dryrun.py --run pipelines/validation/run.example.json
# → exit 3，提示 "非 real 不得当 G3 证据"

# 放行干跑，看六行判定
python3 pipelines/validation/g3_dryrun.py --run pipelines/validation/run.example.json \
    --allow-synthetic --out reports/DRY-001/g3.json
```

一次真实 run 的目录建议：

```
reports/<run_id>/
  check.json          # G1：三平面校验原始输出
  compat.md           # 契约兼容性 diff
  impact.md           # 波及清单（contract-impact）
  audit/              # 污染审计双通道原始输出（n-gram + embedding）
  eval/run.json       # 双跑记录 + 解码参数 + judge_version + holdout_ref
  g3.json             # 六行判定（本脚本产出）
  flywheel.json       # 循环收口重算（FLY-CYCLE，禁止手填）
  evidence.md         # 人读版：契约版本指纹 + 环境 + 结论
```

`eval/run.json` 里必须有的字段（缺了就无法归因，等于没有证据）：`judge_version`、`holdout_ref`、
`decoding{temperature,seed,max_tokens,concurrency}`、`baseline.cost_per_solve`、`runs[]≥2`。

## 5. Go / No-Go 判据

| 结果 | 判决 | 下一步 |
|---|---|---|
| H1 H2 H5 全绿 | **可落地** | 按 F-2026-001 正式开循环（G2 冻结 → G3），21 天期限足够 |
| H1 红（复现偏差超阈） | **不可开循环** | 先做评测工程，这是 GUIDE FAQ 里"还没有可靠自动评测"的同一条；不要用跑通模型来替代 |
| H2 红（泄漏拦不住） | **不可开循环** | 隔离手段先落地；泄漏的模型一律不出现在 KB（S-001 场景 2） |
| H3 红但 H1/H2 绿 | **模式可落地，选题要换** | 换目标子集/维度，本轮作废归档为负结果（`fly_negative_result_published ≥ 1`） |
| H5 红 | **有条件落地** | RB-001 增加"平台前提"章节，或在网关层自建分流后再上线 |
| H6 红（门禁没拦住违规 PR） | **立刻停** | 门禁是这套东西唯一的护城河，先修门禁 |

注意"可落地"不等于"模型变强了"。**失败循环带完整证据同样算通过（E-001 口径）**——这是这套设计最反直觉、
也最值钱的地方：它让"没变好"也变成可复用的资产。

## 6. 六个最容易踩的坑

1. **把干跑证据当真实证据**：`g3_dryrun.py` 默认拒绝判绿就是为这条；合成证据只能落 `reports/DRY-*/`。
2. **温度/并发不写进证据**：H1 红了却无法归因，等于白跑五天。
3. **拿公开 benchmark 直接当 holdout**：基座多半见过，`eval_leak_count` 名义为 0、实际已污染（PIT-001 的隐蔽变体）。
   公开集可以做"探针"，做裁判必须自建或改写，并进 deny-list。
4. **奖励/判分同源自评**：用同一个模型既生成又判分，`RL-VERIFIER.v1` 的独立性就没了（PIT-002 奖励黑客）。
5. **冷启动打穿 SLO**：serverless 的首 token 延迟会让 `MDL-SERVE.x-budget` 的 p99 直接超，探针要分 warm/cold。
6. **边跑边调阈值**：任何"先放宽再跑一次看看"都是换尺子，只能走 CR + `RES-<num>`。

## 7. 明确不做（本轮 out of scope）

- **不做预训练/中训练**（`CORP-PRETRAIN.v1` / `PRE-HEALTH.v1` / `MID-HEALTH.v1`）：租算力做这两段
  既贵又慢，且与"循环是否可信"无关。在 Feature 里声明跳过，别假装验证过。
- **不做 8 卡 vLLM / 双可用区**（`MDL-SERVE.x-deployment`）：那是转正后的容量问题，单卡足以验证语义。
- **不做自动超参/阈值搜索**：F-2026-001 非目标已明令禁止。
- **不追求一轮多目标**：一轮只动一个目标维度，否则增益无法归因。

## 8. 与三平面的接线（要动哪些工件）

| 你的发现 | 该落到哪 | 你能做到哪一步 |
|---|---|---|
| 复现偏差达不到阈值 | `EVAL-BENCH` 的 CR 草稿（破坏性，需 `RES-<num>`） | 只能起草 §1–§3，批准权在委员会（ADR-0001） |
| 平台不支持秒级回滚 | `RB-001` 修订（runbook 可改） | 可提 PR |
| 单卡 QLoRA 的真实成本/吞吐 | `knowledge/capabilities/CARD-002` 补充 | 更新能力卡（provides/consumes 同步） |
| 泄漏/复现的坑 | `knowledge/pitfalls/` 新条目 | `status: candidate`，`provenance: agent:experiment-distiller@<run>` |
| 模型自己提的 mix 配比 | draft CR，`provenance: model:<version>@<episode>` | 不得直接改配置（GUIDE §5 验收信号） |

判决完成后跑一次 `python3 tools/check.py stats`：如果契约场景覆盖率不是 100%、知识新鲜度 <90%，
说明验证过程中的新发现没回流——那这次验证只完成了一半。
