# 1 Log de Bugs e Correções

## Bug #1: Redundância de Argumentos no Serializer

### Identificação
- **Data:** 2025-12-13
- **Reportado por:** Teste Automatizado (Pytest)
- **Severidade:** Média (Impede a execução da API)
- **Módulo:** `posts/serializers.py`

### Descrição
O `EventsSerializer` falhava ao iniciar devido a uma validação estrita do Django Rest Framework. O campo `total_participants` foi definido com o argumento `source='total_participants'`, o que o framework considera um erro de redundância.

### Reprodução
1. Executar o comando de teste: `python -m pytest tests/unit/posts/test_performance_task.py`
2. O sistema tenta carregar a aplicação.
3. **Resultado obtido:** `AssertionError: It is redundant to specify source='total_participants' on field 'IntegerField'...`

### Investigação
**Técnica utilizada:** Análise de Stack Trace.
O erro no terminal indicou explicitamente a linha da falha e a razão. Não foi necessário debugger interativo, pois a mensagem de erro era descritiva.

**Código problemático:**
```python
# posts/serializers.py
total_participants = serializers.IntegerField(
    source="total_participants", read_only=True # ERRO: source igual ao nome do campo
)
```

### Correção
Remoção do argumento `source`, mantendo apenas o `read_only`.

```python
# posts/serializers.py
total_participants = serializers.IntegerField(read_only=True)
```

### Verificação
✓ O teste passou a ser coletado e executado sem erros de importação.

---

## Bug #2: Falha de Configuração de Ambiente (SECRET_KEY)

### Identificação
- **Data:** 2025-12-13
- **Reportado por:** Django Test Runner
- **Severidade:** Alta (Impede inicialização do projeto)
- **Módulo:** `settings.py` / Ambiente de Teste

### Descrição
Ao rodar testes isolados via linha de comando (`python -m pytest`), o Django lançava um erro `ImproperlyConfigured` porque a variável de ambiente `SECRET_KEY` não estava carregada no shell.

### Reprodução
1. Abrir terminal limpo.
2. Rodar: `python -m pytest ...`
3. **Resultado obtido:** `django.core.exceptions.ImproperlyConfigured: The SECRET_KEY setting must not be empty.`

### Investigação
**Técnica utilizada:** Leitura de Logs e Verificação de Variáveis.
Analisamos o traceback e constatamos que o `settings.py` tentava ler `os.environ.get('SECRET_KEY')` e recebia `None`.

### Correção
Injeção da variável de ambiente diretamente na linha de execução do teste.

```bash
SECRET_KEY="chave-temporaria-teste" python -m pytest tests/unit/posts/test_performance_task.py
```

### Verificação
✓ O Django inicializou corretamente e conectou ao banco de dados SQLite.

---

## Bug #3: Falso Positivo em Teste de Performance (Auth 401)

### Identificação
- **Data:** 2025-12-13
- **Reportado por:** Script de Análise de Performance
- **Severidade:** Média (Gera métricas falsas)
- **Módulo:** `tests/unit/posts/test_performance_task.py`

### Descrição
O script de performance retornava **0 queries**, indicando falsamente uma performance perfeita. O problema era que a API retornava erro `401 Unauthorized` antes de consultar o banco, pois o cliente de teste não estava autenticado.

### Reprodução
1. Executar teste com `APIClient` sem login.
2. **Resultado obtido:** Status 401, Queries: 0.

### Investigação
**Técnica utilizada:** Logging Estratégico (Print Debugging).
Adicionamos um `print(response.status_code)` no script, revelando o código 401.

### Correção
Implementação de autenticação forçada no `setUp` do teste.

```python
self.client.force_authenticate(user=self.user)
```

### Verificação
✓ Status code passou a ser 200 e as queries reais (12) apareceram.

---

## Técnicas de Depuração Utilizadas

1. **Análise de Stack Trace:**
   Utilizada primariamente para resolver o Bug #1 (Serializer) e Bug #2 (Settings). A leitura atenta da pilha de chamadas permitiu localizar o arquivo exato e a linha onde a exceção foi levantada.

2. **Logging Estratégico (Print Debugging):**
   Fundamental no Bug #3. Como o erro era lógico (o teste "passava" mas não media nada), o debugger não parava em exceções. Inserir `print()` estratégicos para exibir o `status_code` revelou o comportamento oculto da aplicação.

3. **Isolamento de Testes:**
   Para corrigir o Bug #1, utilizamos a execução isolada de um único arquivo de teste (`pytest tests/unit/posts/...`) em vez de rodar a suíte completa. Isso reduziu o ciclo de feedback de minutos para segundos.