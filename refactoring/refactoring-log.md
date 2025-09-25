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
  - `src/djangoproject/users/services.py` (Criado)
  - `src/djangoproject/users/urls.py` (Modificado)
- **Justificativa**: A lógica de `Follow` e `Unfollow` estava espalhada por duas Views (60+ linhas no total), violando o princípio DRY e o SRP (Views continham lógica de negócio pesada). A lógica foi consolidada em um único método `toggle_user_follow` e movida para um `services.py` para desacoplar a lógica de negócio da camada de apresentação.
- **Resultado**:
  - `FollowUserView` (32 linhas) e `UnfollowUserView` (31 linhas) **removidas**.
  - `toggle_user_follow` (~35 linhas) **criado** no `services.py`.
  - `ToggleFollowUserView` (~18 linhas) **criada** na `views.py`.
- **Impacto**: Redução significativa de código duplicado (~30 linhas). Melhor testabilidade, manutenbilidade e legibilidade devido a redução de código duplicado
- **Testes**: Todos os testes passando

## Refatoração #3: Remoção de código morto

- **ID**: Não identificado
- **Data**: 25/09/2025
- **Autor**: Caio de Medeiros Trindade
- **Code Smell**: Dead Code (Unused Import) em `src/djangoproject/users/serializers.py`
- **Técnica Aplicada**: Remove Dead Code
- **Arquivos Afetados**:
  - `src/djangoproject/users/serializers.py` (Modificado)
  - `src/djangoproject/posts/tests.py` (Modificado)
- **Justificativa**: Remoção de código desnecessário para melhorar a legibilidade e reduzir a complexidade do código-fonte
- **Resultado**:
  - (2 linhas) **removidas**.
- **Impacto**: Remoção de processamento de imports que não estavam sendo utilizados
- **Testes**: Todos os testes passando

## Refatoração #4: Corrigir Argumento de Função Não Utilizado

- **ID**: W0613
- **Data**: 25/09/2025
- **Code Smell**: Unused Parameter / Argumento Não Utilizado
- **Técnica Aplicada**: "Rename Variable" (para convenção de não uso)
- **Arquivos Afetados**: `src/djangoproject/users/views.py`
- **Justificativa**: O método `get` da classe `ListAllUsersView` recebia o parâmetro `request` por herança da `APIView`, mas não o utilizava em sua lógica. Para melhorar a clareza e sinalizar explicitamente que o parâmetro é intencionalmente não utilizado, ele foi renomeado para `_request`, seguindo as convenções da comunidade Python e satisfazendo o `pylint`.
- **Impacto**: Melhoria na legibilidade do código e eliminação de um aviso do linter, deixando o código mais limpo.
- **Testes**: N/A (Refatoração segura que não altera o comportamento da função). -> Então, não será necessário criar um before-after.

## Refatoração #5: Desacoplar Lógica de Consulta da FeedView (SRP)

- **ID**: Não identificado(Violação do SRP)
- **Data**: 25/09/2025
- **Code Smell**: Violação do Princípio da Responsabilidade Única (SRP).
- **Técnica Aplicada**: "Extract Method" (movendo a lógica de consulta para Model Managers customizados).
- **Arquivos Afetados**:
  - `src/djangoproject/posts/views.py` (Modificado)
  - `src/djangoproject/posts/models.py` (Modificado)
- **Justificativa**: A `FeedView` estava fortemente acoplada à lógica de acesso a dados, sabendo _como_ construir as queries complexas tanto para Posts quanto para Eventos, incluindo a lógica de escopo. Isso violava o SRP. A lógica de consulta de cada modelo foi movida para seu respectivo `Manager` (`PostsManager`, `EventsManager`), centralizando e encapsulando as regras de negócio de acesso a dados.
- **Impacto**: A `FeedView` foi simplificada e sua responsabilidade agora é clara: orquestrar a busca de dados e formatar a resposta. As consultas ao banco de dados tornaram-se reutilizáveis e testáveis de forma isolada, melhorando a coesão e o desacoplamento do código.
- **Testes**: Não consideramos necessário. (Refatoração estrutural; comportamento final inalterado).
