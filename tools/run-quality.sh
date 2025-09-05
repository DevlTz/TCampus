#!/usr/bin/env bash
set -euo pipefail

echo "Rodando o formatador de código (black)..."
black --check . || true

echo "Rodando o Flake8"
flake8 || true

echo "Rodando o Pylint para testes - Vai demorar"
pylint --rcfile=.pylintrc || true

echo "Rodando o Cyclomatic Complexity (radon)..."
radon cc -s . || true

echo "Rodando testes especificos (pytest)..."
pytest || true

echo "Done."

