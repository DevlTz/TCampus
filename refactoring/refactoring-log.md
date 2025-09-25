# Log de Refatorações

## Refatoração #1: Consolidar Lógica de Curtir/Deixar de Curtir

- **ID:** R0801
- **Data**: 18/09/2025
- **Autor**: Caio de Medeiros Trindade
- **Code Smell**: Duplicate Code em src/djangoproject/views.py
- **Técnica Aplicada**: Consolidate Duplicate Logic & Move Method (para Camada de Service)]
- **Arquivos Afetados**: src/djangoproject/views.py, src/djangoproject/posts/service.py e src/djangoproject/posts/urls.py
- **Justificativa**: A lógica de Like/Unlike estava duplicada em duas Views (`LikePostView`, `UnlikePostView`), violando o princípio DRY. A lógica foi consolidada em um único método (`toggle_post_like`) e movida para uma camada de serviço (`services.py`), modularizando a lógica de negócio da camada de apresentação (View) e aplicando o SRP.
- **Resultado**:
  toggle_post_like: 15 linhas (em src/djangoproject/posts/service.py)
  class ToggleLikePostView(APIView): 13 linhas (em src/djangoproject/views.py)
- **Impacto**: Melhor testabilidade, manutenbilidade e legibilidade devido a redução de código duplicado
- **Testes**: Todos os testes passando

## Refatoração #2: Consolidar Lógica de Seguir/Deixar de Seguir

- **ID**: R0801
- **Data**: 18/09/2025
- **Autor**: Caio de Medeiros Trindade
- **Code Smell**: Duplicate Code em `src/djangoproject/users/views.py`
- **Técnica Aplicada**: Consolidate Duplicate Logic & Move Method (para Camada de Service)
- **Arquivos Afetados**:
  - `src/djangoproject/users/views.py` (Modificado)
  - `src/djangoproject/users/service.py` (Criado)
  - `src/djangoproject/users/urls.py` (Modificado)
- **Justificativa**: A lógica de `Follow` e `Unfollow` estava espalhada por duas Views (60+ linhas no total), violando o princípio DRY e o SRP (Views continham lógica de negócio pesada). A lógica foi consolidada em um único método `toggle_user_follow` e movida para um `services.py` para desacoplar a lógica de negócio da camada de apresentação.
- **Resultado**:
  - `FollowUserView` (32 linhas) e `UnfollowUserView` (31 linhas) **removidas**.
  - `toggle_user_follow` (~35 linhas) **criado** no `services.py`.
  - `ToggleFollowUserView` (~18 linhas) **criada** na `views.py`.
- **Impacto**: Redução significativa de código duplicado (~30 linhas). Melhor testabilidade, manutenbilidade e legibilidade devido a redução de código duplicado
- **Testes**: Todos os testes passando

## Refatoração #3: Renomear variável não utilizada 

- **ID**: R0802
- **Data**: 23/09/2025
- **Autor**: Luisa Ferreira de Souza Santos
- **Code Smell**: Unused argument em `src/djangoproject/users/views.py`
- **Técnica Aplicada**: Rename Variable
- **Arquivos Afetados**:
  - `src/djangoproject/users/views.py` (Modificado)
- **Justificativa**: Melhorar a clareza da intenção do código, indicando explicitamente que um parâmetro herdado não é necessário para a lógica do método.
- **Resultado**:
  - variável `request`  -> `_request` 
- **Impacto**: Melhora na legibilidade do código, deixando explícito que não é um parâmetro utilizado.
- **Testes**: Todos os testes passando
