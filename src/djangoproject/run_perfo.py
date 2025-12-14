import os
import time
import django
import tracemalloc
from django.conf import settings
from django.test import Client
from django.db import connection

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoproject.settings")
os.environ["SECRET_KEY"] = "chave-123"
# -----------------------------------------

django.setup()
if not settings.DEBUG:
    print("!!! ATIVANDO DEBUG TEMPORARIAMENTE PARA CONTAGEM DE QUERIES !!!")
    settings.DEBUG = True

settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver', '127.0.0.1']  # <<<<
def run_analysis():
    client = Client()
   # url = "/feed" ou events? tá dando erro
    
    print(f"\n--- INICIANDO ANÁLISE: {url} ---\n")

    # --- PARTE 1: DESEMPENHO (TEMPO + QUERIES) ---
    django.db.reset_queries()
    start_time = time.time()
    
    # Faz a requisição
    response = client.get(url)
    
    end_time = time.time()
    queries = len(connection.queries)
    duration = (end_time - start_time) * 1000  # Converte para milissegundos
    
    print(f"[DESEMPENHO] Tempo de resposta: {duration:.2f} ms")
    print(f"[BANCO DE DADOS] Queries executadas: {queries}")
    
    if queries > 10:
        print(">>> ALERTA: Muitas queries! Provável problema de N+1 detectado.")
    else:
        print(">>> SUCESSO: Quantidade de queries otimizada.")

    # --- PARTE 2: MEMÓRIA ---
    print("\n[MEMÓRIA] Analisando pico de memória...")
    tracemalloc.start()
    
    # Roda várias vezes para forçar uso de memória
    for _ in range(30): 
        client.get(url)
        
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"[MEMÓRIA] Pico de uso: {peak / 1024:.2f} KiB")
    print("-" * 30)

if __name__ == "__main__":
    run_analysis()