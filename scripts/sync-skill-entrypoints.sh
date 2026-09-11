#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
canonical="$repo_root/SKILL.md"

targets=(
  "$repo_root/.agents/skills/ceb/SKILL.md"
  "$repo_root/.claude/skills/ceb/SKILL.md"
  "$repo_root/.trae/skills/ceb/SKILL.md"
  "$repo_root/.kimi-code/skills/ceb/SKILL.md"
  "$repo_root/.opencode/skills/ceb/SKILL.md"
)

for target in "${targets[@]}"; do
  mkdir -p "$(dirname -- "$target")"
  cp "$canonical" "$target"
done
