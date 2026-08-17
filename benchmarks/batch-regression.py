#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""多领域全矩阵回归基准入口。

- 提示词: framework/system_prompt.md
- 用例:   cases/<文件>, 默认 cases-multidomain.json

用法:
  API_BASE=<endpoint> API_KEY=<key> MODEL=<model> \
      python3 benchmarks/batch-regression.py [cases.json] [--temps 0.7 1.0] [--reps 3]
"""
import os
import sys
import json
import time
import argparse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from framework.framework import load_prompt, load_cases, list_prompts
from harness.run_harness import chat, verdict

DEFAULT_CASES = "cases-multidomain.json"


def parse_args():
    ap = argparse.ArgumentParser(description="多领域全矩阵回归")
    ap.add_argument("cases_file", nargs="?", default=DEFAULT_CASES,
                    help=f"用例集文件名(cases/ 下),默认 {DEFAULT_CASES}")
    ap.add_argument("--prompt", default="", help="提示词文件名(prompts/ 下),默认用 system_prompt.md")
    ap.add_argument("--temps", nargs="+", type=float, default=[0.7, 1.0],
                    help="温度列表,默认 0.7 1.0")
    ap.add_argument("--reps", type=int, default=3, help="每(用例×温度)遍数,默认 3")
    return ap.parse_args()


def main():
    args = parse_args()
    sys_prompt = load_prompt()
    if args.prompt:
        sys_prompt = load_prompt(os.path.join(ROOT, "prompts", args.prompt))
    cases = load_cases(args.cases_file)
    temps, reps = args.temps, args.reps
    total = len(cases) * len(temps) * reps
    print(f"=== 回归: {args.cases_file} ({len(cases)}用例) × {temps} × {reps}遍 = {total}次 ===", flush=True)

    results = []
    for cid, domain, question in cases:
        for temp in temps:
            for rep in range(1, reps + 1):
                t0 = time.time()
                try:
                    code, resp = chat(sys_prompt, question, temperature=temp,
                                      max_tokens=40000, timeout=280)
                except Exception as e:
                    code, resp = -2, repr(e)
                v, hits = verdict(resp)
                ok = (v == "PASS?" and len(resp or "") > 100)
                results.append({"cid": cid, "domain": domain, "temp": temp, "rep": rep,
                                "code": code, "verdict": v, "ok": ok, "len": len(resp or "")})
                print(f"  [{cid}|{temp}|r{rep}] {domain}: {v} ok={ok} len={len(resp or '')}", flush=True)
        sub = [r for r in results if r["cid"] == cid]
        print(f"  => {cid} ({domain}): {sum(r['ok'] for r in sub)}/{len(sub)}\n", flush=True)

    out = os.path.join(ROOT, "data", "summaries", "regression-summary.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)

    n = len(results); n_ok = sum(r["ok"] for r in results)
    print(f"\n=== 总通过率: {n_ok}/{n} = {100.0*n_ok/n:.1f}% ===")
    print("\n=== 分领域诊断 ===")
    by_domain = {}
    for r in results:
        by_domain.setdefault(r["domain"], []).append(r["ok"])
    for d, oks in by_domain.items():
        print(f"  {d}: {sum(oks)}/{len(oks)}")
    for t in temps:
        sub = [r for r in results if r["temp"] == t]
        print(f"  温度{t}: {sum(r['ok'] for r in sub)}/{len(sub)}")
    print("\n=== DONE ===")


if __name__ == "__main__":
    main()