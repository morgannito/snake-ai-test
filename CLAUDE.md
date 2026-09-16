# snake-ai-test

## Nature / Stack
Banc d'essai d'**aider en boucle autonome** (LLM local) sur un petit jeu Snake Python/pygame — le jeu est le prétexte, `autoloop.sh` est le sujet.
7 fichiers suivis, ~200 lignes de Python. `.venv` local avec l'outillage seul (ruff, mypy 1.20, pytest 9, coverage) sous Python 3.14.3.
État : **abandonné**. Les 6 commits datent tous du 21/04/2026 ; `origin` existe (`git@github.com:morgannito/snake-ai-test.git`) mais aucune branche distante n'est suivie localement.

## Commandes
- Boucle autonome : `./autoloop.sh "<tâche>" [max_iter]` (défauts : `Fix validation errors`, `5`). Elle crée une branche `ai/<epoch>-<slug>`, boucle `validate` → `aider`, et en cas de succès fait `git push -u origin` + `gh pr create` ; sinon `git checkout main` + `git branch -D`.
- Portail de validation (`CONVENTIONS.md`, repris par `autoloop.sh`) : `ruff check .` · `mypy --strict .` (sur `snake_logic.py` uniquement, pas `snake.py`) · `pytest -q`.
- Lancer le jeu : **aucune commande écrite** (le `README.md` ne contient que son titre).

## Architecture
- `snake_logic.py` — logique pure, 3 fonctions : `move_snake`, `check_collision`, `eat_food`.
- `snake.py` — point d'entrée pygame (`main()` sous `if __name__ == "__main__"`), fenêtre 400×400, cellules de 20, rendu + boucle d'événements.
- `test_snake_logic.py` — 4 tests pytest, uniquement sur `snake_logic.py`.
- `autoloop.sh` — la boucle : modèle `openai/mlx-community/Qwen3-8B-4bit` via `OPENAI_API_BASE=http://192.168.50.6:8090/v1` (endpoint LLM du LAN, clé `dummy`), `aider --read CONVENTIONS.md --file snake_logic.py --file test_snake_logic.py`, `timeout 300` par itération.
- `CONVENTIONS.md` — règles injectées dans le prompt d'aider (type hints obligatoires, fonctions < 25 l., logique pure séparée des I/O, pas de `Co-Authored-By`).

## Pièges
- **`snake.py` ne tourne pas** : il appelle `move_snake`, `check_collision` et `eat_food` sans jamais importer `snake_logic` (ses seuls imports sont `pygame` et `random`) → `NameError` au premier tick. Aucun test ne couvre `snake.py`, et `ruff` l'exclut explicitement dans `autoloop.sh` : le défaut passe sous tous les contrôles.
- **Longueur du serpent incohérente** (latent, masqué par le bug ci-dessus) : `move_snake` retire déjà la queue (`snake[:-1]`) et `snake.py` refait un `snake.pop()` quand il n'y a pas de nourriture → le serpent rétrécit en avançant et ne grandit jamais en mangeant.
- **Le portail de validation semble ne pas pouvoir passer en l'état** (constat statique, ruff/mypy/pytest non exécutés ici) : `snake_logic.py` n'a aucune annotation alors que `mypy --strict` le cible, et `test_snake_logic.py` importe `pytest` sans l'utiliser — deux violations directes de `CONVENTIONS.md`. À confirmer en lançant `validate` avant de compter sur une boucle `autoloop.sh`.
- **`pygame` n'est déclaré nulle part** (aucun `requirements.txt` / `pyproject.toml`) et n'est pas installé dans `.venv` : le jeu n'est pas lançable avec `.venv/bin/python`.
- `autoloop.sh` fait `cd ~/projects/snake-ai-test` (minuscule) alors que le dossier réel est `~/Projects/snake-ai-test` ; ça ne passe que grâce à l'insensibilité à la casse d'APFS. Le script a `set -u` mais **pas** `set -e` : ailleurs, le `cd` échoue et la boucle s'exécute dans le répertoire courant.
- `eat_food(head, food, cell_size)` ignore son paramètre `cell_size` (comparaison de position exacte).
- `__pycache__/` est absent du `.gitignore` (qui ne couvre que `.aider*` et `.venv/`) et pollue `git status`.
