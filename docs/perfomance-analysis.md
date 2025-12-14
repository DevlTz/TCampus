# Análise de Desempenho

## Visão Geral
Esta análise foca na otimização de endpoints críticos da API, identificando gargalos de I/O (Banco de Dados) e processamento de resposta.

---

## Gargalo #1: Problema de N+1 Queries (Critical Path)

### Identificação
- **Módulo:** `posts/views.py`
- **Endpoint:** `GET /events/`
- **Problema:** O ORM do Django executava uma consulta SQL separada para buscar os dados do autor (`User`) para cada evento listado na resposta.
- **Impacto:** Degradação linear da performance. Para listar 10 eventos, eram executadas 12 consultas (1 count + 1 select list + 10 selects de autor).

### Medição (Benchmark)
**Ferramenta:** `pytest` + `django.db.connection`

| Métrica | Antes (Baseline) | Depois (Otimizado) | Ganho |
| :--- | :--- | :--- | :--- |
| **Queries SQL** | 12 queries | 2 queries | **83% de redução** |
| **Tempo (Local)**| ~570ms | ~480ms | Variável (Otimização foca em IO) |
| **Escalabilidade**| O(N) | O(1) | Constante |

### Otimização Aplicada
Uso de `Eager Loading` com `select_related` para realizar um SQL JOIN único.

```python
# Antes
queryset = Events.objects.all().order_by("-postedAt")

# Depois
queryset = Events.objects.select_related('postedBy').order_by("-postedAt")
```

---

## Gargalo #2: Ordenação em Coluna Não Indexada

### Identificação
- **Módulo:** `posts/models.py`
- **Funcionalidade:** Feed de Eventos
- **Problema:** A ordenação padrão `.order_by("-postedAt")` é realizada em uma coluna sem índice de banco de dados (`postedAt`).
- **Impacto:** Em tabelas com milhares de registros, o banco precisa fazer um "Full Table Scan" para ordenar os resultados, causando lentidão crescente.

### Análise Teórica
- **Complexidade Atual:** O(N log N) para ordenação em memória ou disco do banco.
- **Solução Proposta:** Adição de índice B-Tree na coluna de data.

### Otimização Documentada
Recomendação de alteração no modelo para incluir indexação:

```python
# posts/models.py
class Events(models.Model):
    # ...
    postedAt = models.DateTimeField(auto_now_add=True, db_index=True) # Recomendação
```

*Nota: Esta otimização foi identificada na análise estática como melhoria futura para escalabilidade.*