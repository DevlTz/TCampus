# Log de Refatorações

## Refatoração #1: Extract Method

- **ID:** R0801
- **Data**: 18/09/2025
- **Autor**: Caio de Medeiros Trindade
- **Code Smell**: Duplicate Code em src/djangoproject/views.py
- **Técnica Aplicada**: Consolidate Duplicate Logic & Move Method (para Camada de Serviço)
- **Justificativa**: A lógica de Like/Unlike estava duplicada em duas Views (`LikePostView`, `UnlikePostView`), violando o princípio DRY. A lógica foi consolidada em um único método (`toggle_post_like`) e movida para uma camada de serviço (`services.py`), modularizando a lógica de negócio da camada de apresentação (View) e aplicando o SRP.
- **Arquivos Afetados**: src/djangoproject/views.py, src/djangoproject/posts/service.py e src/djangoproject/posts/urls.py
- **Resultado**:
  toggle_post_like: 15 linhas (em src/djangoproject/posts/service.py)
  class ToggleLikePostView(APIView): 13 linhas (em src/djangoproject/views.py)
- **Impacto**: Melhor testabilidade e legibilidade
- **Testes**: Todos os testes passando
