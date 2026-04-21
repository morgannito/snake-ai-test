# Conventions projet

## Code
- Type hints obligatoires (Python 3.11+)
- PEP-8 strict, ruff format
- Fonctions < 25 lignes
- Séparer logique pure (no IO) des side-effects
- Pas de commentaires évidents, docstrings courtes si utile
- Pas d'imports inutilisés

## Tests
- Pytest, un fichier `test_*.py` par module
- Un test = un assert principal, nommage `test_<fn>_<scenario>`
- Couverture logique pure ≥ 80%
- Tests indépendants, pas d'état partagé

## Git
- Messages conventionnels : feat:, fix:, refactor:, test:, docs:
- Courts et naturels, pas de Co-Authored-By

## Validation obligatoire avant commit
- `ruff check .`
- `mypy --strict .` (sur snake_logic.py, pas snake.py pygame)
- `pytest -q`
