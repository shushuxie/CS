#!/usr/bin/env bash
# collect_zhihu.sh — delegate to Python orchestrator
set -euo pipefail
WORK="/Users/xieshuqiang/Documents/typora"
exec python3 "$WORK/zhihu/_collect.py" "$@"
