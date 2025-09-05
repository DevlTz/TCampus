[![CI](https://img.shields.io/badge/ci-pending-lightgrey)](https://github.com/)
[![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey)](https://github.com/)
[![license](https://img.shields.io/badge/license-BSL--1.1-orange)](LICENSE)
[![tests](https://img.shields.io/badge/tests-passing-lightgrey)](https://github.com/)

# BPP — Boas Práticas de Programação (MVP)

BPP — MVP em **Django / Python** focado em código limpo, testes, métricas de qualidade e documentação de refatorações.  
**Licença:** Código sob *Business Source License (BSL 1.1)* — uso comercial restrito; documentação sob *CC BY-NC-SA 4.0*.

---

## Índice
- [Sobre](#sobre)  
- [Tecnologias](#tecnologias)  
- [Instalação rápida](#instalação-rápida)  
- [Executando o projeto](#executando-o-projeto)  
- [Qualidade de código](#qualidade-de-código)  
- [Testes](#testes)  
- [Estrutura sugerida do repositório](#estrutura-sugerida-do-repositório)  
- [Contribuição](#contribuição)  
- [Licença](#licença)  
- [Contato / Licenciamento Comercial](#contato--licenciamento-comercial)

---

## Sobre
Repositório para a disciplina **Boas Práticas de Programação (BPP)**. Objetivo: desenvolver um MVP completo em Django com ênfase em:
- código limpo e legível;
- identificação e registro de *code smells*;
- refatorações documentadas (before/after);
- integração contínua com checks de qualidade.

---

## Tecnologias
- Python 3.10+  
- Django (versão indicada em `requirements.txt`)  
- Ferramentas de qualidade: Black, Flake8, Pylint, Radon  
- Testes: pytest / Django test runner  
- CI: template em `.github/workflows/ci.yml`

---

## Instalação rápida

```bash
# clonar o repositório
git clone https://github.com/DevlTz/BPP_MVP.git bpp-mvp
cd bpp-mvp

# criar ambiente virtual
python -m venv .venv
# macOS / Linux
source .venv/bin/activate

# instalar dependências
pip install -r requirements.txt
```
---

## Executando o projeto

```bash
# entrar na pasta src (onde estará o projeto Django)
cd src

# criar projeto Django (se ainda não existir)
django-admin startproject project_name .

# criar app de exemplo
python manage.py startapp core

# aplicar migrações e rodar servidor
python manage.py migrate
python manage.py runserver
```

---

## Qualidade de código
Scripts e recomendações para manter padrão de qualidade:

- `tools/run-quality.sh` — executa checks: `black --check`, `flake8`, `pylint`, `radon cc` e `pytest`.
- Configure o CI (`.github/workflows/ci.yml`) para rodar esses checks em PRs.
- Use `pre-commit` (opcional) para aplicar `black` e `isort` automaticamente.

Exemplo (local):
```bash
# rodar script de qualidade
./tools/run-quality.sh
```

---

## Testes

```bash
# rodar testes com pytest
pytest
# ou com o manage.py
python manage.py test
```

Mantenha cobertura de testes nos módulos críticos e registre métricas de cobertura no CI.

---

## Estrutura sugerida do repositório / Seguindo o PDF do Professor

```
bpp-mvp/
├─ LICENSE                # BSL 1.1 (código)
├─ LICENSE-DOCS           # CC BY-NC-SA 4.0 (documentação)
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ src/
│  ├─ manage.py
│  └─ project_name/
├─ apps/
├─ tests/
├─ docs/
│  ├─ vision.md
│  ├─ backlog.md
│  └─ quality-metrics.md
├─ refactoring/
│  ├─ code-smells-identified.md
│  └─ refactoring-log.md
├─ tools/
│  └─ run-quality.sh
└─ .github/
   └─ workflows/ci.yml
```

---

## Contribuição
Contribuições são bem-vindas, porém seguem estas diretrizes básicas:

1. Abra uma *issue* descrevendo a sugestão/bug/feature.  
2. Crie um *branch* a partir de `main` com nome `feature/<descrição>` ou `fix/<descrição>`.  
3. Submeta um Pull Request referenciando a issue. Inclua testes e justificativa da alteração.  
4. Todas as contribuições serão avaliadas; contribuições aceitas serão mescladas mediante revisão.

Veja `CONTRIBUTING.md` para política completa (inclui CLA/PR policy recomendada).

---

## Licença
- **Código:** Business Source License 1.1 (BSL 1.1). O código é *source-available* mas com restrições de uso comercial conforme texto em `LICENSE`. Leia o arquivo para detalhes e condições, inclusive sobre eventual reversão para licença mais permissiva em data futura.  
- **Documentação (PDFs, guias):** CC BY-NC-SA 4.0 — permite adaptação e compartilhamento não comercial, exige atribuição e ShareAlike. Texto completo em `LICENSE-DOCS`.

---

## Contato / Licenciamento Comercial
Uso comercial ou redistribuição para fins comerciais requer autorização explícita dos autores. Para propostas de licenciamento comercial ou dúvidas legais, contate os mantenedores listados no arquivo `AUTHORS.md` ou envie um email para o responsável (informações de contato no repositório).

---
