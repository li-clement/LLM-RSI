#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TriPlane 三平面一致性校验器（G1 门禁的执行体）。

用法：
  python3 tools/check.py [lint] [--strict]   # 校验；--strict 时警告也算失败
  python3 tools/check.py stats [--changed "f1 f2 ..."]
                                             # 三平面健康度仪表盘
仅依赖 Python 3.9+ 标准库。校验规则与 specs/README.md、knowledge/README.md 一致。
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FEATURE_STATUS = {"draft", "in-review", "approved", "frozen", "released"}
EPIC_STATUS = FEATURE_STATUS
CONTRACT_STATUS = {"active", "deprecated"}
KNOWLEDGE_STATUS = {"candidate", "accepted", "retired", "superseded", "proposed"}
SCENARIO_STATUS = {"draft", "accepted", "retired"}
FLAVOR_KIND = {"openapi": "api", "asyncapi": "event", "schema": "dataset", "model": "model", "eval": "eval"}
DIR_TYPE = {
    "domain": "glossary",
    "capabilities": "capability",
    "decisions": "decision",
    "patterns": "pattern",
    "pitfalls": "pitfall",
    "runbooks": "runbook",
}
CONTRACT_NAME_RE = re.compile(r"^(?P<id>[A-Z]{2,8}-[A-Z0-9]+)\.v(?P<major>\d+)\.(?P<flavor>openapi|asyncapi|schema|model|eval)\.json$")
STEM_ID_RE = re.compile(r"^(?P<id>[A-Z]{2,6}-[0-9]{1,4}|[A-Z]{2,6}-[0-9]{4})(?=(-|$))")

errors: list = []
warnings: list = []


def err(where: str, msg: str) -> None:
    errors.append(f"ERROR {where}: {msg}")


def warn(where: str, msg: str) -> None:
    warnings.append(f"WARN  {where}: {msg}")


def unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def parse_frontmatter(path: Path):
    """极简 YAML 子集：顶层 key、字符串、内联列表 [a, b]、块列表（- x）。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fm = {}
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            return fm
        s = line.rstrip()
        if not s or s.lstrip().startswith("#"):
            continue
        if not s.startswith(" ") and s.lstrip().startswith("- "):
            if key is not None and isinstance(fm.get(key), list):
                fm[key].append(unquote(s.strip()[2:]))
            continue
        if ":" in s and not s.startswith(" "):
            k, _, v = s.partition(":")
            k, v = k.strip(), v.strip()
            if v == "":
                fm[k] = []
                key = k
            elif v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                fm[k] = [unquote(x) for x in inner.split(",") if x.strip()] if inner else []
                key = None
            else:
                fm[k] = unquote(v)
                key = None
    return None  # 未见结束 ---


def need(fm: dict, where: str, keys: list) -> bool:
    missing = [k for k in keys if fm.get(k) in (None, "")]
    for k in missing:
        err(where, f"frontmatter 缺少必填字段 `{k}`")
    return not missing


def stem_id_ok(fm_id: str, path: Path, where: str) -> None:
    if fm_id != path.stem and not path.stem.startswith(fm_id + "-"):
        err(where, f"id `{fm_id}` 与文件名 `{path.stem}` 不一致")


def parse_date(v):
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        return None


# ---------------------------------------------------------------- contracts

def load_contracts():
    contracts = {}  # "ID.vN" -> dict
    cdir = ROOT / "specs" / "contracts"
    if not cdir.is_dir():
        err("specs/contracts", "契约目录不存在")
        return contracts
    for path in sorted(cdir.glob("*.json")):
        where = str(path.relative_to(ROOT))
        m = CONTRACT_NAME_RE.match(path.name)
        if not m:
            err(where, "文件名必须符合 <ID>.v<major>.<openapi|asyncapi|schema>.json")
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(where, f"JSON 解析失败: {e}")
            continue
        xc = doc.get("x-contract")
        if not isinstance(xc, dict):
            err(where, "缺少 x-contract 元数据（契约事实必须内嵌，无 sidecar）")
            continue
        need(xc, where, ["id", "kind", "version", "status", "owner", "consumers", "compatibility", "steward"])
        cid, major, flavor = m.group("id"), int(m.group("major")), m.group("flavor")
        if xc.get("id") != cid:
            err(where, f"x-contract.id `{xc.get('id')}` != 文件名 id `{cid}`")
        if xc.get("kind") != FLAVOR_KIND[flavor]:
            err(where, f"kind `{xc.get('kind')}` 与 flavor `{flavor}` 不匹配（应为 {FLAVOR_KIND[flavor]}）")
        ver = str(xc.get("version", ""))
        if ver.split(".")[0] != str(major):
            err(where, f"x-contract.version `{ver}` 主版本 != 文件名 v{major}")
        if flavor == "openapi":
            if "openapi" not in doc:
                err(where, "文档缺少 `openapi` 版本根字段")
            if doc.get("info", {}).get("version") and str(doc["info"]["version"]).split(".")[0] != str(major):
                err(where, "info.version 主版本与文件名不一致")
        elif flavor == "asyncapi":
            if "asyncapi" not in doc:
                err(where, "文档缺少 `asyncapi` 版本根字段")
        elif flavor == "schema":
            if "$schema" not in doc and doc.get("type") != "object":
                err(where, "数据集契约必须是 JSON Schema（$schema 或 type: object）")
            sla = doc.get("x-sla")
            if not isinstance(sla, dict) or not sla.get("cadence") or not sla.get("min_count"):
                err(where, "数据集契约必须声明 x-sla（cadence / freshness_days / min_count）")
            if not doc.get("x-quality"):
                err(where, "数据集契约必须声明至少一条 x-quality 质量断言——没有断言的数据集不是资产，是负债")
        elif flavor == "eval":
            if xc.get("approval") != "committee":
                err(where, "评测契约的 x-contract.approval 必须为 committee——阈值冻结权在治理委员会（换尺子防线）")
            proto = doc.get("x-protocol")
            missing = [k for k in ("benchmark", "metrics", "thresholds", "isolation") if not isinstance(proto, dict) or not proto.get(k)]
            if missing:
                err(where, f"评测契约 x-protocol 缺少节: {missing}")
            elif not isinstance(proto.get("thresholds"), dict):
                err(where, "x-protocol.thresholds 必须是 metric -> 阈值 的映射")
        elif flavor == "model":
            for ext in ("x-signature", "x-budget", "x-fallback"):
                if not doc.get(ext):
                    err(where, f"模型契约必须声明 {ext}（接口签名 / 成本与延迟预算 / 降级策略）")
        status = xc.get("status")
        if status not in CONTRACT_STATUS:
            err(where, f"status `{status}` 非法（{sorted(CONTRACT_STATUS)}）")
        if status == "deprecated" and not xc.get("sunset"):
            warn(where, "deprecated 契约应声明 sunset 日期")
        consumers = xc.get("consumers") or []
        if not isinstance(consumers, list) or not consumers:
            err(where, "consumers 必须为非空数组（没有消费者的接口不是契约，是私货）")
        if xc.get("owner") in consumers:
            err(where, "owner 不应同时出现在 consumers 中")
        key = f"{cid}.v{major}"
        if key in contracts:
            err(where, f"契约重复定义 `{key}`")
        contracts[key] = {"file": where, "xc": xc, "id": cid, "major": major, "doc": doc}
    return contracts


# ---------------------------------------------------------------- knowledge

def load_knowledge():
    knowledge = {}  # id -> dict
    for dname, etype in DIR_TYPE.items():
        d = ROOT / "knowledge" / dname
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.md")):
            if path.name == "README.md":
                continue
            where = str(path.relative_to(ROOT))
            fm = parse_frontmatter(path)
            if fm is None:
                err(where, "缺少 frontmatter（复制 templates/knowledge-item.md）")
                continue
            need(fm, where, ["id", "type", "title", "scope", "confidence", "status", "owner", "provenance"])
            kid = fm.get("id", path.stem)
            if path.name == "CONTEXT.md" and dname == "domain":
                pass  # 术语表是规范固定文件名，引用点遍布三平面，豁免 stem 一致性
            else:
                stem_id_ok(kid, path, where)
            if fm.get("type") != etype:
                err(where, f"type `{fm.get('type')}` 与目录 `knowledge/{dname}/`（{etype}）不符")
            if fm.get("status") not in KNOWLEDGE_STATUS:
                err(where, f"status `{fm.get('status')}` 非法")
            if fm.get("confidence") not in {"high", "medium", "low"}:
                err(where, f"confidence `{fm.get('confidence')}` 非法")
            if not fm.get("provenance"):
                err(where, "provenance 不能为空——无出处的知识不收")
            if etype == "decision":
                if fm.get("status") not in {"proposed", "accepted", "superseded"}:
                    err(where, "decision 状态只能是 proposed/accepted/superseded")
                if fm.get("status") == "accepted" and not fm.get("date"):
                    err(where, "accepted 的 ADR 必须有 date")
                if not re.match(r"^ADR-\d{4}$", str(kid)):
                    err(where, "ADR id 必须形如 ADR-0001")
            else:
                exp = parse_date(fm.get("expires", ""))
                if exp is None:
                    err(where, "缺少或非法的 expires（TTL）")
                elif exp < datetime.date.today():
                    err(where, f"知识已过期（expires={exp}）——复核后更新 expires 或置 retired")
                elif (exp - datetime.date.today()).days <= 30:
                    warn(where, f"TTL 将于 {exp} 到期（≤30 天），安排 Curator 复核")
            if etype == "capability":
                need(fm, where, ["bu", "provides", "consumes", "contact"])
            if kid in knowledge:
                err(where, f"知识 id 重复 `{kid}`")
            knowledge[kid] = {"file": where, "fm": fm, "type": etype}
    return knowledge


def check_capability_vs_contracts(knowledge, contracts):
    bus = {}
    for kid, item in knowledge.items():
        if item["type"] == "capability":
            bus[item["fm"].get("bu")] = item
    for kid, item in knowledge.items():
        if item["type"] != "capability":
            continue
        fm, where = item["fm"], item["file"]
        for c in fm.get("provides", []):
            if c not in contracts:
                err(where, f"provides 引用不存在的契约 `{c}`")
            elif contracts[c]["xc"].get("owner") != fm.get("bu"):
                err(where, f"provides `{c}` 与契约 owner BU（{contracts[c]['xc'].get('owner')}）不符")
        for c in fm.get("consumes", []):
            if c not in contracts:
                err(where, f"consumes 引用不存在的契约 `{c}`")
            elif fm.get("bu") not in (contracts[c]["xc"].get("consumers") or []):
                err(where, f"consumes `{c}` 但该 BU 不在契约 consumers 名单中")
    for ckey, c in contracts.items():
        owner = c["xc"].get("owner")
        if owner not in bus:
            warn(c["file"], f"owner BU `{owner}` 没有能力卡（新 BU 必须先发卡）")
            continue
        owned = [k for k, v in contracts.items() if v["xc"].get("owner") == owner]
        provide_set = bus[owner]["fm"].get("provides", [])
        for k in owned:
            if k not in provide_set:
                err(bus[owner]["file"], f"契约 {k} 声明你为 owner，但能力卡 provides 未列出")
        for consumer in c["xc"].get("consumers", []):
            if consumer not in bus:
                warn(c["file"], f"consumer BU `{consumer}` 没有能力卡")
            elif ckey not in bus[consumer]["fm"].get("consumes", []):
                err(bus[consumer]["file"], f"契约 {ckey} 声明 {consumer} 为 consumer，但能力卡 consumes 未列出")


# ---------------------------------------------------------------- specs

def load_specs(contracts, knowledge):
    features, epics, scenarios = {}, {}, {}
    sdir = ROOT / "specs"

    for path in sorted((sdir / "epics").glob("*.md")) if (sdir / "epics").is_dir() else []:
        if path.name == "README.md":
            continue
        where = str(path.relative_to(ROOT))
        fm = parse_frontmatter(path)
        if fm is None:
            err(where, "缺少 frontmatter")
            continue
        need(fm, where, ["id", "title", "status", "bu", "features", "owner"])
        stem_id_ok(fm.get("id", ""), path, where)
        if fm.get("status") not in EPIC_STATUS:
            err(where, f"status `{fm.get('status')}` 非法")
        for f in fm.get("features", []):
            features_ref.add(f)
        epics[fm.get("id")] = {"file": where, "fm": fm}

    fdir = sdir / "features"
    for path in sorted(fdir.glob("*.md")) if fdir.is_dir() else []:
        if path.name == "README.md":
            continue
        where = str(path.relative_to(ROOT))
        fm = parse_frontmatter(path)
        if fm is None:
            err(where, "缺少 frontmatter（复制 templates/feature-spec.md）")
            continue
        need(fm, where, ["id", "title", "epic", "status", "bu", "contracts", "knowledge", "owner"])
        stem_id_ok(fm.get("id", ""), path, where)
        if not re.match(r"^F-\d{4}-\d+$", str(fm.get("id"))):
            err(where, "Feature id 必须形如 F-2026-001")
        if fm.get("status") not in FEATURE_STATUS:
            err(where, f"status `{fm.get('status')}` 非法")
        if fm.get("status") in {"frozen", "released"} and not parse_date(fm.get("frozen_at", "")):
            err(where, "frozen/released 必须带 frozen_at 日期")
        if fm.get("epic") not in epics:
            err(where, f"引用不存在的 Epic `{fm.get('epic')}`")
        for c in fm.get("contracts", []):
            if c not in contracts:
                err(where, f"引用不存在的契约 `{c}`")
            else:
                contract_ref.add(c)
                involved = {contracts[c]["xc"].get("owner")} | set(contracts[c]["xc"].get("consumers", []))
                if not involved & set(fm.get("bu", [])):
                    warn(where, f"契约 `{c}` 的 owner/consumers 与本 Feature 的 bu 无交集")
        for k in fm.get("knowledge", []):
            if k not in knowledge:
                err(where, f"引用不存在的知识项 `{k}`")
            else:
                knowledge_ref.add(k)
        for b in fm.get("bu", []):
            if b not in bu_codes:
                err(where, f"BU 代码 `{b}` 没有对应能力卡（先补 knowledge/capabilities/）")
        if fm.get("id") in features:
            err(where, f"Feature id 重复 `{fm.get('id')}`")
        features[fm.get("id")] = {"file": where, "fm": fm}

    for eid, e in epics.items():
        for f in e["fm"].get("features", []):
            if f not in features:
                err(e["file"], f"Epic 引用不存在的 Feature `{f}`")
            elif features[f]["fm"].get("epic") != eid:
                warn(features[f]["file"], f"Feature 的 epic=`{features[f]['fm'].get('epic')}` 与 Epic `{eid}` 的 features 列表不互指")
        for b in e["fm"].get("bu", []):
            if b not in bu_codes:
                err(e["file"], f"BU 代码 `{b}` 没有对应能力卡")

    sdir2 = sdir / "scenarios"
    for path in sorted(sdir2.glob("*.md")) if sdir2.is_dir() else []:
        if path.name == "README.md":
            continue
        where = str(path.relative_to(ROOT))
        fm = parse_frontmatter(path)
        if fm is None:
            err(where, "缺少 frontmatter（复制 templates/scenario.md）")
            continue
        need(fm, where, ["id", "kind", "status", "executable", "runner"])
        stem_id_ok(fm.get("id", ""), path, where)
        if not re.match(r"^S-\d+$", str(fm.get("id"))):
            err(where, "Scenario id 必须形如 S-001")
        if fm.get("status") not in SCENARIO_STATUS:
            err(where, f"status `{fm.get('status')}` 非法")
        kind = fm.get("kind")
        if kind == "acceptance":
            if fm.get("feature") not in features:
                err(where, "acceptance 场景必须引用存在的 Feature（`feature:`）")
            else:
                scenario_ref.add(fm["feature"])
        elif kind == "contract":
            if fm.get("contract") not in contracts:
                err(where, "contract 场景必须引用存在的契约（`contract:`，形如 ORD-PAID.v1）")
            else:
                contract_scenario_ref.add(fm["contract"])
        else:
            err(where, f"kind `{kind}` 非法（acceptance|contract）")
        if fm.get("id") in scenarios:
            err(where, f"Scenario id 重复 `{fm.get('id')}`")
        scenarios[fm.get("id")] = {"file": where, "fm": fm}

    for ckey, c in contracts.items():
        if ckey not in contract_scenario_ref:
            err(c["file"], "契约没有任何 kind:contract 的契约场景——没有消费者测试的契约不允许存在")
    for fid, f in features.items():
        acc = [s for s in scenarios.values() if s["fm"].get("kind") == "acceptance" and s["fm"].get("feature") == fid]
        if not acc:
            err(f["file"], "Feature 没有任何 kind:acceptance 的验收场景")
    return features, epics, scenarios


# ---------------------------------------------------------------- entry

features_ref, contract_ref, contract_scenario_ref, knowledge_ref, scenario_ref = set(), set(), set(), set(), set()
bu_codes = set()


def load_agents_entry():
    p = ROOT / "AGENTS.md"
    if not p.is_file():
        err("AGENTS.md", "缺失——Agent 一等公民入口是三平面的一部分")
        return
    fm = parse_frontmatter(p)
    if fm is None or not fm.get("mode"):
        warn("AGENTS.md", "frontmatter 应声明 mode（如 triplane/0.1）")


def cmd_lint(strict: bool) -> int:
    load_agents_entry()
    contracts = load_contracts()
    knowledge = load_knowledge()
    bu_codes.update(k["fm"].get("bu") for k in knowledge.values() if k["type"] == "capability")
    check_capability_vs_contracts(knowledge, contracts)
    load_specs(contracts, knowledge)

    for line in errors:
        print(line)
    for line in warnings:
        print(line)
    ok = not errors and (not warnings or not strict)
    print(f"\n三平面校验：{len(errors)} 错误 / {len(warnings)} 警告 "
          f"（契约 {len(contracts)} · 知识 {len(knowledge)}）")
    print("G1 " + ("✅ 通过" if ok else "❌ 不通过"))
    return 0 if ok else 1


def cmd_stats(changed: str) -> int:
    load_agents_entry()
    contracts = load_contracts()
    knowledge = load_knowledge()
    bu_codes.update(k["fm"].get("bu") for k in knowledge.values() if k["type"] == "capability")
    check_capability_vs_contracts(knowledge, contracts)
    features, epics, scenarios = load_specs(contracts, knowledge)

    cids = sorted({c["id"] for c in contracts.values()})
    cov = [c for c in cids if any(k.split(".v")[0] == c for k in contract_scenario_ref)]
    frozen = [f for f, v in features.items() if v["fm"].get("status") in {"frozen", "released"}]
    today = datetime.date.today()
    fresh, expiring = [], []
    for kid, item in sorted(knowledge.items()):
        exp = parse_date(item["fm"].get("expires", "")) if item["type"] != "decision" else None
        if exp is None:
            fresh.append(kid)
        elif exp >= today:
            fresh.append(kid)
            if (exp - today).days <= 30:
                expiring.append(f"{kid}（{exp}）")
    accepted = [k for k, v in knowledge.items() if v["fm"].get("status") == "accepted"]
    text = "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "specs").rglob("*.md"))
    text += "\n".join(p.read_text(encoding="utf-8") for p in (ROOT / "specs" / "contracts").glob("*.json"))
    unreferenced = [k for k in accepted if k not in knowledge_ref and not re.search(rf"\b{re.escape(k)}\b", text)]

    print("TriPlane 健康度仪表盘")
    print(f"  Epic {len(epics)} · Feature {len(features)}（frozen/released: {len(frozen)}）· 契约 {len(cids)} 个 ID / {len(contracts)} 个版本 · 场景 {len(scenarios)} · 知识 {len(knowledge)}")
    print(f"  契约场景覆盖率: {len(cov)}/{len(cids)}")
    print(f"  知识新鲜度: {len(fresh)}/{len(knowledge)}" + (f" · 30 天内到期: {', '.join(expiring)}" if expiring else ""))
    print(f"  未被消费的 accepted 知识（90 天规则观察项）: {', '.join(unreferenced) if unreferenced else '—'}")
    if changed:
        print("\n  变更关联分析（--changed）:")
        for f in changed.split():
            m = CONTRACT_NAME_RE.match(Path(f).name)
            if m:
                ckey = f"{m.group('id')}.v{m.group('major')}"
                consumers = contracts.get(ckey, {}).get("xc", {}).get("consumers", [])
                print(f"    {ckey}: 契约场景 {[s['fm']['id'] for s in scenarios.values() if s['fm'].get('contract') == ckey]} · 消费方 {consumers}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", nargs="?", default="lint", choices=["lint", "stats"])
    ap.add_argument("--strict", action="store_true", help="警告也视为失败")
    ap.add_argument("--changed", default="", help="stats：空格分隔的变更文件路径，输出关联分析")
    a = ap.parse_args()
    return cmd_stats(a.changed) if a.command == "stats" else cmd_lint(a.strict)


if __name__ == "__main__":
    sys.exit(main())
