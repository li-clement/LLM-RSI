# 使用指南（TriPlane · RSI 工具箱）

> MODE.md 回答"模式是什么"，本文回答"**明天开始怎么用**"。所有路径、命令在仓库根目录执行。

## 0. 30 秒版

1. 冷启动：先填**能力卡 + 术语表**，再把**现有评测口径**誊成 `EVAL-BENCH` 草案——这三样决定一切。你在生命周期哪个环节（采集/CORP/SFT/RL/RAG/飞轮 × 预训练/中训练/后训练）？查[场景化契约族地图](specs/contracts/README.md)。
2. 日常：跨团队说"好"之前，先让 `python3 tools/check.py` 说"绿"。
3. 铁律：契约 frozen 后只能走 CR；评测阈值只有委员会能改；Agent 与 RSI 自提案只能起草不能批准。

---

## 1. 按角色读什么、做什么

| 你是谁 | 先读 | 第一件事 | 日常动作 |
|---|---|---|---|
| 团队负责人 / 委员会 | [MODE.md](MODE.md) §1–2、§6 | 确认三权分立（[ADR-0001](knowledge/decisions/ADR-0001-eval-authority-separation.md)）是否照单全收，不收就改 ADR 再开工 | 月度：处置 eval CR、看 `stats` 与元指标；季度：能力卡盘点 |
| Cycle Owner（循环轮值） | [specs/README.md](specs/README.md) + [templates/feature-spec.md](templates/feature-spec.md) | 把下一轮循环写成 Feature（目标/地板/预算/期限） | §3-A 全流程 |
| Dataset / Model Steward | [specs/contracts/README.md](specs/contracts/README.md) | 把本团队最痛的接口誊成第一份契约并挂契约场景 | 审 CR、值守兼容性 diff、执行冻结联签 |
| Eval Steward | [EVAL-BENCH.v1](specs/contracts/EVAL-BENCH.v1.eval.json) + [S-004](specs/scenarios/S-004-eval-bench-contract.md) | 把现有评测脚本的指标/阈值/holdout 规则誊成协议草案 | 拒绝私下评测请求；出 G3 证据 |
| Knowledge Curator | [knowledge/README.md](knowledge/README.md) | 建周会日历（30 分钟，只处置 candidate） | §3-D 回流与复核 |
| Release Steward | [RB-001](knowledge/runbooks/RB-001-model-promotion-rollback.md) + [PAT-001](knowledge/patterns/PAT-001-champion-challenger.md) | 确认 champion 热备机制在位（回滚 <60s 的前提） | 主持 G4 联签与灰度 |
| 工程师 / 结对 Agent | [AGENTS.md](AGENTS.md) | 跑 `check.py` 拿三平面地图 | 写代码前先加载 Feature 的 `knowledge:` 清单 |

---

## 2. 冷启动：前 14 天

**第 1–2 天 · 骨架就位**

```bash
# 把本仓库拷成公司级 Spec 仓库（名字随意，下文称 triplane-rsi）
# 初始化后第一件事：让门禁上线，哪怕此时只有示例
python3 tools/check.py --strict && echo ok
```

把示例链挪出校验区，留作填空范本（check.py 只扫固定工件目录，`_examples` 自动出局；规则文档 README.md 留在原位）：

```bash
mkdir -p specs/_examples knowledge/_examples observability/_examples
mv specs/epics specs/features specs/scenarios specs/contracts specs/_examples/
mv knowledge/domain knowledge/capabilities knowledge/decisions \
   knowledge/patterns knowledge/pitfalls knowledge/runbooks knowledge/_examples/
mv observability/dashboards observability/_examples/   # metric 契约挪走前，board 会引用失败——一起挪
# 重建空工件目录（check.py 要求 specs/contracts 存在；git 不跟踪空目录时可放 .gitkeep）
mkdir -p specs/{epics,features,contracts,scenarios} \
         knowledge/{domain,capabilities,decisions,patterns,pitfalls,runbooks}
python3 tools/check.py --strict && echo "空骨架也守规矩：G1 ✅"
```

真实工件就位后，重写 `observability/dashboards/` 下的 board（范本在 `_examples/`）。

**第 3–5 天 · 三张底牌**

1. **团队代码表 + 术语表**：照 [CONTEXT.md](knowledge/domain/CONTEXT.md) 的结构，先只填你们真实的团队码和 10 个最容易吵的词（"成功""污染""回归"各团队定义往往不同——这一步最值钱）。
2. **能力卡**：每个团队一张（[模板](templates/capability-card.md)），`provides/consumes` 允许先为空。
3. **评测口径誊写**：把散在脚本里的指标、阈值、holdout 清单誊成 `EVAL-BENCH.v1.eval.json` 草案（[规则](specs/contracts/README.md)）。誊不出来的部分 = 你们真正的评测债，列成待办。

**第 6–10 天 · 第一份真契约**

选一个最近出过事故的数据接口或模型接口，写 dataset/model/event 契约 + ≥1 个契约场景（[模板](templates/scenario.md)）。跑 `check.py` 绿，把 P1 CI 挂上（[specrepo-ci.yml](pipelines/ci/specrepo-ci.yml)）。

**第 11–14 天 · 第一次冻结演练**

用 §3-A 流程对一个**小循环**（一周能跑完的那种）走 `draft → frozen`。第一次做全流程，目标不是快，是让每个角色把手感走一遍。

---

## 3. 日常操作流

### A. 开一轮改进循环（Cycle Owner）

```
1  cp templates/feature-spec.md specs/features/F-<年>-<num>-<slug>.md
2  填循环规格四要素：目标维度（引用 EVAL 指标 ID）/ 回归地板 / 预算 / 期限
3  读上一轮 reports/<cycle>/flywheel.json——目标必须从数据来（S-008 #5）
4  PR → 其他团队 Steward 评论确认职责切分表 → status: approved
5  冻结 PR：status: frozen + frozen_at；四方联签；P1 绿后合并（G2 完成）
6  循环期间：任何想改口径的冲动 → 转成 CR 草稿，不动 frozen 契约
```

### B. 契约变更（任何团队，含"换尺子"）

```
1  cp templates/contract-change.md → PR 标题必须含 CR-<num>（G1 会检查）
2  contract-impact Agent 预生成 §3 波及清单 → 各消费方确认
3  分类自查：
   非破坏（加可选字段/收紧 SLO）→ 对方 Steward 审核即可
   破坏（删字段/收窄枚举/改口径）→ 新 major + 旧 sunset ≥90 天 + 双跑方案
   尺子（EVAL 指标/阈值/judge 版本）→ 一律破坏性 + PR 描述带委员会决议号 RES-<num>
4  新契约场景同 PR 提交；消费方测试补丁由 test-weaver 出 draft PR
5  关闭后：sunset 前每季度看旧版本流量（stats 点名）
```

### C. 加指标 / 上仪表盘（顺序不可反）

```
1  先在 metric 契约里定义：id/def/unit + slo（观察型标 informational: true）
   没有阈值先别加——没有阈值的指标只是数字
2  实现采集：发射点写进 x-telemetry.collect；与数据集断言同源的指标用 binds（只搬运，禁二次实现）
3  面板进 observability/dashboards/*.board.json：每个 panel 必须有 metric + source
4  check.py 会拦：裸名上板、指标 ID 跨契约重复、alert 引用未注册指标
```

### D. 知识回流与复核（Curator）

```
触发即候选：CR 关闭 / 事故复盘 / 循环收口（含失败）/ crit 告警连续两周期
1  experiment-distiller 自动开 candidate PR（confidence 上限 medium）
2  周会 30 分钟只做处置：accepted / 合并进既有 ID / 拒绝（拒绝也要留理由评论）
3  复核清单见 templates/knowledge-item.md（重叠？有消费场景？探测落到流水线哪一步？）
4  TTL：stats 会列 30 天内到期项——复核顺手续约（被新 Feature 引用 = 自动延长一周期）
```

### E. 线上熔断与回滚（Release Steward / 值班）

直接照 [RB-001](knowledge/runbooks/RB-001-model-promotion-rollback.md) 执行：触发条件 → 切回 champion（<60s，热备在位是前提）→ **冻结本轮循环**（Feature 回退，不追加临时变更）→ 24h 内事故材料喂 distiller。严禁现场调阈值"再看一次"。

---

## 4. 命令速查 & 报错对照

```bash
python3 tools/check.py            # lint，默认模式
python3 tools/check.py --strict   # G1：警告也算失败（CI 用这个）
python3 tools/check.py stats      # 健康度：覆盖率/新鲜度/未消费知识/指标注册数
python3 tools/check.py stats --changed "specs/contracts/SFT-PAIRS.v1.schema.json"
                                  # 变更关联分析：契约场景 + 消费方
```

| check.py 报错 | 意思 | 修法 |
|---|---|---|
| `缺少 frontmatter` | 工件没写元数据 | 复制 [templates/](templates/) 对应模板 |
| `契约没有任何 kind:contract 的契约场景` | 契约裸奔 | 写 S-xxx（[模板](templates/scenario.md)） |
| `id 与文件名不一致` | 引用货币错乱 | 按 [specs/README.md](specs/README.md) ID 规则改名 |
| `评测契约的 approval 必须为 committee` | 试图让 Steward 管尺子 | 加字段；变更走委员会 |
| `指标必须声明 slo 或 informational` | 裸数字上契约 | 定阈值或承认它是观察指标 |
| `面板引用未定义指标` / `指标 ID 跨契约冲突` | 裸名/双源 | 先定义再上板；保留一个源另一个用 binds |
| `能力卡 provides/consumes 未列出` | 能力地图 ≠ 现实 | 同步卡片（这就是设计意图：逼你更新地图） |
| `知识已过期（expires=…）` | TTL 到期 | 复核 → 更新 expires 或置 retired |
| `引用不存在的契约/知识项` | ID 拼错或已删 | 修引用或补建工件 |
| `frozen/released 必须带 frozen_at` | 状态跃迁缺证据 | 填冻结日期 |

---

## 5. Agent 接入

**IDE 结对**：仓库根目录的 [AGENTS.md](AGENTS.md) 会被主流编码 Agent 自动加载。确认它的加载顺序（§2）被执行：先 `check.py`，再契约，再知识，最后才是代码。

**流水线内嵌**：[agents/playbooks.md](agents/playbooks.md) 的 8 个任务书按 CI 占位 job 接线（[pipelines/ci/](pipelines/ci/)）。接入顺序建议：`cycle-summarizer`（零风险，只评论）→ `assertion-forge`（省写测试）→ `experiment-distiller`（喂知识平面）。

**RSI 自提案**（你们项目的特殊项）：模型生成的 mix 建议、训练补丁、接口变更草稿一律走 [model-ci](pipelines/ci/model-ci.example.yml) 的 `self-proposal-inbox` 通道 → draft CR，`provenance: model:<version>@<episode>`。**验收信号**：自提案出现在 CR 待办里而不是直接改配置——出现直接改配置的，管道有洞。

---

## 6. 怎么算"模式跑起来了"（30 天自检）

- [ ] `check.py --strict` 在 Spec 仓库 CI 上常绿 ≥2 周
- [ ] 至少 1 个真实循环走完 G2 → G3（哪怕失败——失败循环归档了证据也算）
- [ ] `stats`：契约场景覆盖率 100%；知识新鲜度 ≥90%
- [ ] 至少 1 条 distiller 候选知识被处置（accepted 或被明确拒绝）
- [ ] 发生过 ≥1 次"P1 拦下了一个未走 CR 的契约变更"（门禁被验证有效）
- [ ] 会议时长下降：跨团队讨论转移为 PR 评论（问卷自查即可）

六条全勾 → 进入常态运营；任何一条长期勾不上 → 回 [MODE.md §9 反模式](MODE.md) 对照自查，通常是门禁太多或指标没绑阈值。

---

## 7. FAQ

**Q：小改动（加一个可选字段）也要 CR？**
是，但非破坏 CR 就是"提 PR + 对方 Steward 评论批准"两步，机器 diff 兜底。流程成本是恒定的，事故成本是长尾的。

**Q：循环跑到一半，需求变了怎么办？**
契约不许动（frozen 语义）。两个选项：本轮作废归档（负结果入库）开新循环；或本轮只加不改（新字段走非破坏 CR，新语义下轮生效）。

**Q：我们还没有可靠的自动评测？**
先别开循环。S1 立靶的前提是 `EVAL-BENCH` 可信——先做 2–3 周评测建设（可复用 [S-004](specs/scenarios/S-004-eval-bench-contract.md) 的断言清单），这是整套模式的地基。

**Q：多个 Epic / 多个循环能并行吗？**
能。引用 ID 天然隔离（每个循环 frozen 自己的契约版本）；但**同一契约被两个在跑循环同时提 CR** 时按先到先得，后者等 frozen 基线更新——这是 `cycle-summarizer` 的"是否触碰在跑基线"评论的用武之地。

**Q：示例链要不要留着？**
挪到 `_examples/`（见 §2）当填空范本。ID 体系（E-001/F-2026-001/契约 ID）会被你们的真实工件复用，别混放。

**Q：想改模式规则本身（比如加第六道门禁）？**
MODE.md 也是工件：改它走 PR + 委员会评审。模式自己遵守"改规则要走谈判"——这就是 dogfooding。
