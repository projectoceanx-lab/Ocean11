#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

errors=0
canonical_agents=(fury scout shield hawk forge watchtower peter ocean)
required_files=(SOUL.md MISSIONS.md config.yaml IDENTITY.md)

echo "== Agent Alignment Validation =="

echo "-- Checking deprecated IDs in config/openclaw.yaml"
deprecated_hits="$(rg -n '\b(captain|signal)\b' config/openclaw.yaml || true)"
if [[ -n "$deprecated_hits" ]]; then
  echo "ERROR: Deprecated IDs found in config/openclaw.yaml:"
  echo "$deprecated_hits"
  errors=1
else
  echo "OK: No deprecated IDs found."
fi

echo "-- Checking required files for canonical agents"
for agent in "${canonical_agents[@]}"; do
  for file in "${required_files[@]}"; do
    path="agents/${agent}/${file}"
    if [[ ! -f "$path" ]]; then
      echo "ERROR: Missing required file: $path"
      errors=1
    fi
  done
done

echo "-- Checking soul paths in config/openclaw.yaml"
soul_paths="$(awk '/^[[:space:]]*soul:[[:space:]]*/ {print $2}' config/openclaw.yaml | sed -e 's/"//g' -e "s/'//g")"
while IFS= read -r soul; do
  [[ -z "$soul" ]] && continue
  repo_path="${soul#./}"
  if [[ ! -f "$repo_path" ]]; then
    echo "ERROR: Invalid soul path in config/openclaw.yaml -> $soul"
    errors=1
  fi
done <<< "$soul_paths"

echo "-- Optional runtime comparison (~/.openclaw/openclaw.json)"
if [[ -f "$HOME/.openclaw/openclaw.json" ]]; then
  runtime_ids="$(python3 - <<'PY'
import json
import os

path = os.path.expanduser("~/.openclaw/openclaw.json")
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)

ids = []
for agent in data.get("agents", {}).get("list", []):
    agent_id = agent.get("id")
    if agent_id == "main":
        agent_id = "fury"
    if agent_id:
        ids.append(agent_id)

print("\n".join(sorted(set(ids))))
PY
)"
  canonical_sorted="$(printf '%s\n' "${canonical_agents[@]}" | sort -u)"

  missing_in_runtime="$(comm -23 <(echo "$canonical_sorted") <(echo "$runtime_ids"))"
  extra_in_runtime="$(comm -13 <(echo "$canonical_sorted") <(echo "$runtime_ids"))"

  if [[ -n "$missing_in_runtime" ]]; then
    echo "ERROR: Runtime is missing canonical IDs:"
    echo "$missing_in_runtime"
    errors=1
  else
    echo "OK: Runtime includes all canonical IDs."
  fi

  if [[ -n "$extra_in_runtime" ]]; then
    echo "WARN: Runtime has extra IDs not in canonical list:"
    echo "$extra_in_runtime"
  fi
else
  echo "INFO: Runtime config not found at ~/.openclaw/openclaw.json (skipping runtime diff)."
fi

if [[ "$errors" -ne 0 ]]; then
  echo "Validation failed."
  exit 1
fi

echo "Validation passed."
