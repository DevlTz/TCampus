#!/usr/bin/env bash
set -euo pipefail
# Allow CODE_DIR to be set via environment variable or first command-line argument, fallback to default
CODE_DIR="${CODE_DIR:-${1:-../src/djangoproject/}}"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' 

echo "Diretório analisado: $CODE_DIR"
ls "$CODE_DIR"

echo -e "${CYAN}==> Rodando Black (formatador) em $CODE_DIR...${NC}"
black --check --diff "$CODE_DIR" || echo -e "${YELLOW}Black encontrou arquivos não formatados!${NC}"

echo -e "${CYAN}==> Rodando Vulture (código morto) em $CODE_DIR...${NC}"
vulture "$CODE_DIR" || echo -e "${YELLOW}Vulture encontrou código não utilizado!${NC}"

echo -e "${CYAN}==> Rodando Flake8 (linter) em $CODE_DIR...${NC}"
flake8 "$CODE_DIR" || echo -e "${RED}Flake8 encontrou problemas!${NC}"

echo -e "${CYAN}==> Rodando Pylint em $CODE_DIR...${NC}"
pylint --rcfile=.pylintrc "$CODE_DIR" || echo -e "${RED}Pylint encontrou problemas!${NC}"

echo -e "${CYAN}==> Rodando Radon (complexidade ciclomática) em $CODE_DIR...${NC}"
radon cc -s "$CODE_DIR" || echo -e "${YELLOW}Radon encontrou funções complexas!${NC}"

echo -e "${CYAN}==> Rodando Pytest em $CODE_DIR...${NC}"
pytest "$CODE_DIR" || echo -e "${RED}Alguns testes falharam!${NC}"

echo -e "${GREEN}Análise de qualidade finalizada! Veja os avisos acima para detalhes.${NC}"