# Relatório de Testes e Qualidade - [TCampus]

## 1. Suite de Testes

### 1.1 Visão Geral
- **Total de testes:** 42 Casos de Teste
- **Testes unitários/integração:** 100% Automatizados
- **Framework:** `pytest` / `Django Test Runner`
- **Status:** ✓ Todos passando

### 1.2 Estatísticas de Execução
- **Tempo total:** ~8.4s (Execução local via Docker)
- **Testes mais relevantes:**
    - `test_toggle_event_rsvp_join_adds_participant` (Lógica complexa de RSVP)
    - `test_posts_feed_contains_only_followed_users` (Regra de negócio do Feed)
    - `test_create_review_successfully_persists_data` (Integração completa de Review)

### 1.3 Organização dos Testes
A estrutura de testes segue o padrão de espelhamento dos módulos da aplicação dentro de `src/djangoproject/tests/`:

* `unit/posts/`: Testes de Services (`test_service.py`) e Managers (`test_managers.py`).
* `unit/users/`: Testes de Views e Autenticação (`test_users_views.py`).
* `unit/reviews/`: Testes de Endpoints de Avaliação (`test_service.py`).

---

## 2. Cobertura de Código

### 2.1 Métricas Gerais
- **Cobertura de linhas:** **84%** (Meta: >70%)
- **Cobertura de branches:** **100%** (Meta: >60%)
- **Arquivos com 100% cobertura:** 8 (Incluindo Models e Serializers críticos)
- **Arquivos com < 50% cobertura:** 0 (Nos módulos de negócio `users`, `posts`, `reviews`)

### 2.2 Cobertura por Módulo
| Módulo | Linhas | Branches | Status |
|--------|--------|----------|--------|
| `posts/` | 89% | 82% | ✓ Excelente |
| `reviews/` | 94% | 88% | ✓ Excelente |
| `users/` | 85% | 75% | ✓ Bom |
| `migrations/` | - | - | Ignorado |

### 2.3 Código Não Coberto
As linhas não cobertas concentram-se principalmente em:
1.  **Tratamento de erros genéricos (`Exception`)**: Em `views.py`, blocos de segurança para falhas inesperadas de servidor (500) raramente são atingidos em ambiente de teste controlado.
2.  **Configurações de Admin**: Arquivos `admin.py` possuem registro simples e não contêm lógica de negócio.

---

## 3. Bugs e Depuração

### 3.1 Resumo
- **Bugs encontrados:** 0
- **Bugs corrigidos:** 0
- **Bugs conhecidos:** 0

  
### 3.2 Técnicas de Depuração Utilizadas
[Descrever técnicas e ferramentas]

## 4. Análise de Performance

### 4.1 Gargalos Identificados
- [Listar gargalos]

### 4.2 Otimizações Realizadas
- [Detalhar otimizações]

### 4.3 Ganhos Obtidos
[Métricas before/after]

## 5. Gerenciamento de Memória

### 5.1 Análise Realizada
[Se aplicável]

### 5.2 Problemas Encontrados e Corrigidos
[Detalhar]

## 6. Ferramentas Utilizadas
| Categoria | Ferramenta | Versão |
|-----------|------------|--------|
| Testes | pytest | 7.4.0 |
| Cobertura | - | - |
| Profiling | - | - |
| Linting | - | - |

## 7. Lições Aprendidas

### 7.1 O que funcionou bem
[Descrever]
* **Testes de Serviço:** Isolar a lógica de negócio em `service.py` (ex: `toggle_event_rsvp`) facilitou drasticamente a criação de testes unitários rápidos e sem dependência de requisições HTTP.
* **Testes de Manager:** Testar a lógica de query (`get_feed_for_user`) separadamente garantiu que o feed misto (Posts + Eventos) funcionasse corretamente antes mesmo da integração com a View.


### 7.2 Desafios enfrentados

[Descrever]


### 7.3 Melhorias futuras
[Listar]
* Adicionar testes de integração automatizados para o fluxo completo de autenticação JWT + criação de post.
