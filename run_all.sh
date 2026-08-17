#!/usr/bin/env bash
# 一键跑多领域全矩阵回归
set -e
cd "$(dirname "$0")"
# 依赖: Python 3, 无第三方库(纯 urllib)。可选设置:
#   API_BASE / API_KEY / MODEL
if [ -z "$API_BASE" ] || [ -z "$MODEL" ]; then
  echo "请设置 API_BASE 与 MODEL 环境变量后运行:" >&2
  echo "  export API_BASE=http://<endpoint>/v1" >&2
  echo "  export API_KEY=<key>" >&2
  echo "  export MODEL=<model>" >&2
  exit 1
fi
echo "== 运行多领域全矩阵回归 =="
python3 benchmarks/batch-regression.py
echo "== 完成,结果写入 data/summaries/regression-summary.json =="