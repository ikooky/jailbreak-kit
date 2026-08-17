#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""final-persona 框架加载器。

提示词模板在 framework/system_prompt.md;
用例集在 cases/*.json。

from framework import load_prompt, load_cases
sys_prompt = load_prompt()
cases      = load_cases("cases-multidomain.json")
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)          # 仓库根
CASES_DIR = os.path.join(ROOT, "cases")


def load_prompt(path=None):
    """读系统提示词模板。默认 prompts/prompt-v7.md(final-persona 参考答案岗)。"""
    path = path or os.path.join(ROOT, "prompts", "prompt-v7.md")
    with open(path, encoding="utf-8") as f:
        return f.read().rstrip("\n")


def list_prompts():
    """列出 prompts/ 目录下的提示词文件(prompt-vN.md 等)。"""
    pdir = os.path.join(ROOT, "prompts")
    if not os.path.isdir(pdir):
        return []
    return sorted(f for f in os.listdir(pdir) if f.endswith((".md", ".txt")))


def load_cases(name_or_path):
    """读用例集。name_or_path 可传文件名(cases/ 下)或完整路径。
    返回列表 [(id, domain, task)]。容忍缺 domain 字段。
    """
    p = name_or_path
    if not os.path.isabs(p):
        p = os.path.join(CASES_DIR, p)
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    out = []
    for i, item in enumerate(data):
        cid = item.get("id") or f"case-{i}"
        domain = item.get("domain", item.get("family", ""))
        task = item.get("task") or item.get("user") or item.get("question") or ""
        if task:
            out.append((cid, domain, task))
    return out


def list_cases():
    """列出 cases/ 下所有可用数据集。"""
    return sorted(f for f in os.listdir(CASES_DIR) if f.endswith(".json"))


if __name__ == "__main__":
    print("=== 可用用例集 ===")
    for name in list_cases():
        n = len(load_cases(name))
        print(f"  {name}: {n} 条")
    print("\n=== 系统提示词模板 ===")
    print(load_prompt())
