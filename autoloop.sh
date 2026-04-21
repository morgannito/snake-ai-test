#!/bin/bash
# Autonomous coding loop avec: git branch, validation étendue, retry, prompt cache
set -u
cd ~/projects/snake-ai-test
export OPENAI_API_BASE=http://192.168.50.6:8090/v1
export OPENAI_API_KEY=dummy

TASK="${1:-Fix validation errors}"
MAX_ITER="${2:-5}"
BRANCH="ai/$(date +%s)-$(echo "$TASK" | tr -c 'a-zA-Z0-9' '-' | cut -c1-30)"

# Crée une branche pour cette tâche — pas de main cassé
git checkout -b "$BRANCH"
echo "=== Branche: $BRANCH — tâche: $TASK ==="

validate() {
  # 3 checks, concat des erreurs
  {
    .venv/bin/ruff check --exclude snake.py . 2>&1 || true
    .venv/bin/mypy --strict --ignore-missing-imports snake_logic.py 2>&1 || true
    .venv/bin/pytest -q --no-header 2>&1 || true
  } | tail -30
}

for i in $(seq 1 "$MAX_ITER"); do
  echo "=== Iter $i/$MAX_ITER ==="
  OUT=$(validate)
  RUFF_OK=$(.venv/bin/ruff check --exclude snake.py . >/dev/null 2>&1 && echo ok)
  MYPY_OK=$(.venv/bin/mypy --strict --ignore-missing-imports snake_logic.py >/dev/null 2>&1 && echo ok)
  PYTEST_OK=$(.venv/bin/pytest -q >/dev/null 2>&1 && echo ok)
  if [ -n "$RUFF_OK" ] && [ -n "$MYPY_OK" ] && [ -n "$PYTEST_OK" ]; then
    echo "✅ TOUT VALIDE"
    git push -u origin "$BRANCH" 2>&1 | tail -2
    gh pr create --title "$TASK" --body "Autonomous PR. Iter $i. ruff+mypy+pytest ✅" --head "$BRANCH" 2>&1 | tail -2
    exit 0
  fi
  echo "ruff=$RUFF_OK mypy=$MYPY_OK pytest=$PYTEST_OK"
  ERR=$(echo "$OUT" | head -40)

  timeout 300 aider --model openai/mlx-community/Qwen3-8B-4bit \
    --no-show-model-warnings --yes-always --auto-commits \
    --no-analytics --no-stream --edit-format whole \
    --no-show-release-notes --map-tokens 0 \
    --cache-prompts \
    --read CONVENTIONS.md \
    --file snake_logic.py --file test_snake_logic.py \
    --message "Task: $TASK

Validation errors:
$ERR

Fix according to CONVENTIONS.md. Respect type hints, keep functions pure.
/no_think" 2>&1 | tail -3
done

echo "❌ $MAX_ITER itérations, rollback"
git checkout main
git branch -D "$BRANCH"
exit 1
