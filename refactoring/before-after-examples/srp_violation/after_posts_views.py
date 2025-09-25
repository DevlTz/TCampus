class FeedView(ListAPIView):
    # A responsabilidade de mesclar e ordenar os dados é da View
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        """
        Gera um feed combinado de posts e eventos.
        - Posts: Sempre de usuários que o usuário atual segue.
        - Eventos: O escopo pode ser alterado via query param '?events_scope=all'.
          - 'following' (padrão): Eventos de usuários seguidos.
          - 'all': Apenas eventos futuros de TODOS os usuários.
        """
        user = request.user
        scope = request.query_params.get('events_scope', 'following')

        # A View delega a busca dos dados para os Managers, que, encapsulam a lógica de consulta
        posts_qs = Posts.objects.get_feed_for_user(user)
        events_qs = Events.objects.get_feed_for_user(user, scope=scope)

        # Serializa os dados obtidos para prepará-los para a resposta.
        posts_data = PostsSerializer(posts_qs, many=True, context={"request": request}).data
        events_data = EventsSerializer(events_qs, many=True, context={"request": request}).data

        # Normaliza as listas de posts e eventos em um formato comum para ordenação.
        normalized = []
        for p in posts_data:
            normalized.append({
                "type": "post",
                "sort_date": p.get("postedAt"), # Data de postagem para ordenar
                "data": p
            })
        for e in events_data:
            normalized.append({
                "type": "event",
                "sort_date": e.get("event_date"), # Data do evento para ordenar
                "data": e
            })

        # Ordena a lista combinada pela data, do mais novo para o mais antigo
        normalized.sort(key=lambda x: x.get("sort_date") or "", reverse=True)
        
        # Constrói o feed final, adicionando o campo "type" a cada objeto
        feed = [item["data"] | {"type": item["type"]} for item in normalized]

        return Response(feed)