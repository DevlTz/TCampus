[![CI](https://img.shields.io/badge/ci-pending-lightgrey)](https://github.com/)
[![coverage](https://img.shields.io/badge/coverage-unknown-lightgrey)](https://github.com/)
[![license](https://img.shields.io/badge/license-BSL--1.1-orange)](LICENSE)
[![tests](https://img.shields.io/badge/tests-passing-lightgrey)](https://github.com/)

# Programming Best Practices (MVP)

Programming Best Practices — MVP in **Django / Python** focused on clean code, testing, quality metrics, and refactoring documentation.  
**License:** Code under *Business Source License (BSL 1.1)* — restricted commercial use; documentation under *CC BY-NC-SA 4.0*.

---

## Table of Contents
- [About](#about)  
- [Technologies](#technologies)  
- [Quick Installation](#quick-installation)  
- [Running the Project](#running-the-project)  
- [Code Quality](#code-quality)  
- [Testing](#testing)  
- [Suggested Repository Structure](#suggested-repository-structure)  
- [Contributing](#contributing)  
- [License](#license)  
- [Contact / Commercial Licensing](#contact--commercial-licensing)

---

## About
Repository for the **Programming Best Practices** course. Goal: develop a complete MVP in Django with emphasis on:
- clean and readable code;
- identification and logging of *code smells*;
- documented refactorings (before/after);
- continuous integration with quality checks.

---

## Technologies
- Python 3.10+  
- Django (version specified in `requirements.txt`)  
- JWT
- Docker
- Quality tools: Black, Flake8, Pylint, Radon, Vulture
- Testing: pytest / Django test runner  
- CI: template in `.github/workflows/ci.yml`

---

## Quick Installation

```bash
# clone the repository
git clone https://github.com/DevlTz/TCampus.git
cd TCampus

# create virtual environment
python -m venv .venv
# macOS / Linux
source .venv/bin/activate

# install dependencies
pip install -r src/requirements.txt -r requirements-dev.txt
```
---

## Running the Project

```bash
# enter the src folder (where the Django project will be)
cd src

# Docker compose 
docker-compose up --build

# apply migrations and run server
docker-compose exec django-web python manage.py  makemigrations
docker-compose exec django-web python manage.py migrate

```

---

## Code Quality
Scripts and recommendations to maintain code quality standards:

- `tools/run-quality.sh` — runs checks: `black --check`, `flake8`, `pylint`, `radon cc`, `pytest`, and `vulture`.
- Configure CI (`.github/workflows/ci.yml`) to run these checks on PRs.
- Optionally use `pre-commit` to automatically apply `black` and `isort`.

Example (local):
```bash
# run quality script
./tools/run-quality.sh
```

---

## Testing

```bash
# run tests with pytest
pytest
# or with manage.py
python manage.py test
```

Maintain test coverage on critical modules and record coverage metrics in CI.

---

## Repository Structure

```
TCampus/
├─ .gitignore
├─ APACHE-2.0-HEADER.md
├─ AUTHORS.md
├─ CONTRIBUTING.md
├─ LICENSE                # BSL 1.1 (code)
├─ LICENSE-DOCS           # CC BY-NC-SA 4.0 (documentation)
├─ NOTICE
├─ README.md
├─ refactoring/
│  ├─ reports/
│  ├─ before-after-examples/
│  ├─ code-smells-identified.md
│  └─ refactoring-log.md
│  └─ docs/
│     ├─ Arq_Diagram.png
│     └─ ERD_Diagram.png
├─ requirements.txt
├─ requirements-dev.txt
├─ src/
│  ├─ .gitignore
│  ├─ Dockerfile
│  ├─ djangoproject/
│  │  ├─ djangoproject/
│  │  │  ├─ __init__.py
│  │  │  ├─ asgi.py
│  │  │  ├─ settings.py
│  │  │  ├─ urls.py
│  │  │  └─ wsgi.py
│  │  ├─ manage.py
│  │  ├─ posts/
│  │  │  ├─ __init__.py
│  │  │  ├─ admin.py
│  │  │  ├─ apps.py
│  │  │  ├─ migrations/
│  │  │  │  ├─ 0001_initial.py
│  │  │  │  ├─ ...
│  │  │  │  └─ __init__.py
│  │  │  ├─ models.py
│  │  │  ├─ serializers.py
│  │  │  ├─ tests.py
│  │  │  ├─ urls.py
│  │  │  └─ views.py
│  │  └─ users/
│  │     ├─ __init__.py
│  │     ├─ admin.py
│  │     ├─ apps.py
│  │     ├─ migrations/
│  │     │  ├─ 0001_initial.py
│  │     │  ├─ 0002_auto_...
│  │     │  ├─ ...
│  │     │  └─ 0007_alter_user_managers.py
│  │     ├─ models.py
│  │     ├─ serializers.py
│  │     ├─ tests.py
│  │     ├─ urls.py
│  │     └─ views.py
│  ├─ docker-compose.yml
│  ├─ manage.py
└─ tools/
   └─ run-quality.sh
```
---
'
## Contributing
Contributions are welcome, but must follow these basic guidelines:

1. Open an *issue* describing your suggestion/bug/feature.  
2. Create a *branch* from `main` named `feature/<description>` or `fix/<description>`.  
3. Submit a Pull Request referencing the issue. Include tests and justification for the change.  
4. All contributions will be reviewed; accepted contributions will be merged after review.

See `CONTRIBUTING.md` for the full policy (includes recommended CLA/PR policy).

---

## License
- **Code:** Business Source License 1.1 (BSL 1.1). The code is *source-available* but with commercial use restrictions as described in `LICENSE`. Read the file for details and conditions, including possible future conversion to a more permissive license.  
- **Documentation (PDFs, guides):** CC BY-NC-SA 4.0 — allows adaptation and non-commercial sharing, requires attribution and ShareAlike. Full text in `LICENSE-DOCS`.

---

## Contact / Commercial Licensing
Commercial use or redistribution for commercial purposes requires explicit authorization from the authors. For commercial licensing proposals or legal questions, contact the maintainers listed in `AUTHORS.md` or send an email to the responsible party (contact information in the repository).

---
