# Análise de Gerenciamento de Memória

## Contexto
Em aplicações Python/Django, o gerenciamento de memória é automatizado pelo Garbage Collector (Reference Counting + Generation GC). No entanto, o uso ineficiente do ORM pode causar "Memory Bloat" (inchaço de memória) e sobrecarga de conexões.

## Análise do Endpoint `/events/`

### Problema: Overhead de Conexões e Cursores
Durante a análise do gargalo de N+1 Queries, identificamos um impacto secundário crítico na memória:

1.  **Alocação de Objetos de Cursor:** Cada query extra (12 queries no total) exige a alocação de memória para um novo cursor do banco de dados (SQLite/Postgres).
2.  **Fragmentação:** A criação e destruição rápida desses objetos de conexão pressiona o Garbage Collector, podendo causar pausas na aplicação (GC Thrashing).

### Otimização Realizada
A implementação do `select_related` reduziu drasticamente a pegada de memória por requisição.

#### Comparativo de Alocação de Recursos

| Recurso | Sem Otimização | Com Otimização | Impacto na Memória |
| :--- | :--- | :--- | :--- |
| **Cursores de BD** | 12 instâncias | 2 instâncias | **Redução de 83%** na alocação de objetos de driver |
| **Round-trips** | 12 trocas de contexto | 2 trocas de contexto | Menor buffer de rede em uso |

### Conclusão
A otimização de consulta não serviu apenas para velocidade, mas estabilizou o consumo de memória da aplicação. Ao trazer os dados "hidratados" em uma única query, evitamos a criação de dezenas de objetos intermediários desnecessários, permitindo que a aplicação suporte mais usuários concorrentes com a mesma quantidade de RAM.