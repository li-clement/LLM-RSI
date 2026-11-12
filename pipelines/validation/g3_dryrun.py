#!/usr/bin/env python3
"""G3 门禁干跑器（零 GPU，纯 stdlib）。

用途：在租到任何算力之前，先用**合成证据**把 G3 的判定逻辑跑一遍，
证明"门禁本身是活的"，并暴露证据字段缺口。这是无自有服务器时
唯一零成本、当天可完成的可落地性探测（见 LANDABILITY-001 H1/H2/H6）。

两条设计约束（对齐三平面）：

1. 阈值不在本文件定义：一律从 specs/contracts/EVAL-BENCH.v1.eval.json 读取
   （单一事实源；改阈值只能走 CR + 委员会决议，见 ADR-0001）。
2. 合成证据必须自带 evidence_kind=synthetic-dryrun；默认**拒绝判绿**，
   防止干跑产物被误用为真实 G3 证据。

用法：
  python3 pipelines/validation/g3_dryrun.py --run pipelines/validation/run.example.json
  python3 pipelines/validation/g3_dryrun.py --run pipelines/validation/run.example.json \
      --allow-synthetic --out reports/DRY-001/g3.json

退出码：0 = G3 绿；1 = G3 红；2 = 输入/契约错误；3 = 拒绝判绿（合成证据未放行）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL_CONTRACT = ROOT / "specs" / "contracts" / "EVAL-BENCH.v1.eval.json"

_NUM = re.compile(r"[-+]?\d+(?:\.\d+)?")


def parse_threshold(expr: str):
    """'>= +3.0pp' / '== 0' / '<= 0.3pp' / '<= champion x 1.1' -> (op, value, factor)"""
    m = re.match(r"^\s*(>=|<=|==)\s*(.+?)\s*$", str(expr))
    if not m:
        raise ValueError(f"无法解析阈值表达式: {expr!r}")
    op, rhs = m.group(1), m.group(2)
    if "champion" in rhs:
        return op, None, float(_NUM.search(rhs).group())
    return op, float(_NUM.search(rhs).group()), None


def compare(observed: float, expr: str, baseline: float | None = None):
    op, target, factor = parse_threshold(expr)
    if factor is not None:
        if baseline is None:
            raise ValueError(f"阈值 {expr!r} 需要 champion 基线值")
        target = baseline * factor
    if op == ">=":
        ok = observed >= target
    elif op == "<=":
        ok = observed <= target
    else:
        ok = abs(observed - target) < 1e-9
    return ok, target


def load_contract(path: Path = EVAL_CONTRACT) -> dict:
    if not path.is_file():
        raise SystemExit(f"找不到评测契约: {path}")
    doc = json.loads(path.read_text(encoding="utf-8"))
    return {
        "id": doc["x-contract"]["id"],
        "version": doc["x-contract"]["version"],
        "thresholds": doc["x-protocol"]["thresholds"],
        "contamination_budget": doc["x-protocol"]["benchmark"]["contamination_budget"],
        "holdout_size_min": doc["x-protocol"]["benchmark"]["holdout_size_min"],
        "judge_pin_required": True,
    }


def evaluate(run: dict, contract: dict) -> dict:
    ev = run["eval"]
    base, chal = ev["baseline"], ev["challenger"]
    targets = [float(r["target"]) for r in ev["runs"]]
    if len(targets) < 2:
        raise ValueError("G3 要求双跑：eval.runs 至少 2 条记录")
    # 双跑差值：>=2 次独立运行取极差（比两点差更保守）
    repro_gap = round(max(targets) - min(targets), 4)

    obs = {
        "target_gain": float(chal["target_gain"]),
        "regression_dims": float(chal["regression_dims"]),
        "cost_per_solve": float(chal["cost_per_solve"]),
        "reproducibility_gap": repro_gap,
    }
    baseline_for = {"cost_per_solve": float(base["cost_per_solve"])}

    th = contract["thresholds"]
    rows, hard_fail = [], []

    # --- G3 三硬条件（pipelines/README.md 五道门禁表）---
    leak = float(run["audit"]["eval_leak_count"])
    ok, tgt = compare(leak, f"== {contract['contamination_budget']}")
    rows.append(("G3.污染审计 eval_leak_count", leak, f"== {tgt:g}", ok, "hard"))
    if not ok:
        hard_fail.append("污染审计未过：challenger 不得进入 KB，须产出负结果候选知识（S-001 场景 2）")

    ok, tgt = compare(obs["reproducibility_gap"], th["reproducibility_gap"])
    rows.append(("G3.复现偏差 reproducibility_gap", obs["reproducibility_gap"], th["reproducibility_gap"], ok, "hard"))
    if not ok:
        hard_fail.append(
            f"复现偏差 {obs['reproducibility_gap']}pp > {tgt}pp：先查温度/seed/并发/判分器版本，"
            "再考虑是否要提 CR（换尺子必须委员会决议）"
        )

    sc = run["scenarios"]
    pass_rate = sc["passed"] / sc["total"] if sc["total"] else 0.0
    ok = pass_rate == 1.0
    rows.append(("G3.契约场景通过率", pass_rate, "== 1.0", ok, "hard"))
    if not ok:
        hard_fail.append("契约场景未 100%：P3 收敛不成立，禁止发起 KB")

    # --- 转正口径（目标/地板/成本）：G3 绿后由 G4 联签消费 ---
    ok, tgt = compare(obs["target_gain"], th["target_gain"])
    rows.append(("转正.target_gain", obs["target_gain"], th["target_gain"], ok, "promotion"))

    ok, tgt = compare(obs["regression_dims"], th["regression_dims"])
    rows.append(("转正.regression_dims", obs["regression_dims"], th["regression_dims"], ok, "promotion"))

    ok, tgt = compare(obs["cost_per_solve"], th["cost_per_solve"], baseline_for["cost_per_solve"])
    rows.append(("转正.cost_per_solve", obs["cost_per_solve"], f"<= {tgt:.4g}", ok, "promotion"))

    return {
        "verdict": "green" if not hard_fail else "red",
        "contract": f"{contract['id']}@{contract['version']}",
        "observed": obs,
        "rows": rows,
        "blocking": hard_fail,
    }


def render(result: dict) -> str:
    width = max(len(r[0]) for r in result["rows"]) + 2
    lines = [f"契约 {result['contract']}  ·  G3 判定：{result['verdict'].upper()}", "-" * 72]
    for name, observed, limit, ok, scope in result["rows"]:
        mark = "✅" if ok else ("❌" if scope == "hard" else "⚠️ ")
        shown = f"{observed:.4g}" if isinstance(observed, float) else str(observed)
        lines.append(f"{mark} {name:<{width}} 实测 {shown:<10} 阈值 {limit:<14} [{scope}]")
    if result["blocking"]:
        lines.append("-" * 72)
        lines.extend(f"  ↳ {b}" for b in result["blocking"])
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="G3 门禁干跑（零 GPU）")
    ap.add_argument("--run", required=True, help="run 证据 JSON 路径")
    ap.add_argument("--out", help="写出判定结果的路径（如 reports/DRY-001/g3.json）")
    ap.add_argument("--allow-synthetic", action="store_true", help="放行合成证据（仅限干跑目录）")
    args = ap.parse_args(argv)

    run_path = Path(args.run)
    if not run_path.is_absolute():
        run_path = ROOT / run_path
    run = json.loads(run_path.read_text(encoding="utf-8"))

    kind = run.get("evidence_kind", "")
    if kind != "real":
        if not args.allow_synthetic:
            print(
                f"拒绝判绿：evidence_kind={kind!r}（非 real）。\n"
                "干跑产物不得当 G3 证据用；确认只做机制演练后加 --allow-synthetic，"
                "并把结果落到 reports/DRY-*/。",
                file=sys.stderr,
            )
            return 3

    contract = load_contract()
    result = evaluate(run, contract)
    result["run_id"] = run.get("run_id")
    result["evidence_kind"] = kind
    print(render(result))

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"\n已写出 {out_path.relative_to(ROOT)}")

    return 0 if result["verdict"] == "green" else 1


if __name__ == "__main__":
    sys.exit(main())
