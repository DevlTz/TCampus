import time
import pytest
from django.utils import timezone
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.db import connection, reset_queries
from django.test import override_settings
from posts.models import Events as ModelTestado

User = get_user_model()
URL_TESTE = "/events/"

@override_settings(DEBUG=True)
class PerformanceAnalysisTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='tester', email='t@t.com', password='123')
        self.client.force_authenticate(user=self.user)
        
        print("\nCreating test data...")
        itens = []
        now = timezone.now()
        for i in range(50):
            item = ModelTestado(
                postedBy=self.user,
                title=f"Event {i}",
                locate="Online",
                event_date=now
            )
            itens.append(item)
        ModelTestado.objects.bulk_create(itens)
        print("Data created.")

    def test_performance_analysis(self):
        print(f"\n--- INICIANDO ANÁLISE: {URL_TESTE} ---")

        # Limpa contagem anterior e garante que está vazio
        reset_queries()
        start_time = time.time()

        # FAZ A REQUISIÇÃO
        response = self.client.get(URL_TESTE)

        end_time = time.time()
        
        # Métricas
        total_queries = len(connection.queries)
        duration = (end_time - start_time) * 1000

        print(f"\n[RESULTADO] Status Code: {response.status_code}")
        print(f"[DESEMPENHO] Tempo: {duration:.2f} ms")
        print(f"[BANCO] Queries: {total_queries}")

        if total_queries > 10:
            print(">>> ALERTA: N+1 Detectado! (Muitas queries)")
        else:
            print(">>> SUCESSO: Otimizado!")
        
        print("-" * 30)