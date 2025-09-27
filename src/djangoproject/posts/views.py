from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Posts, Events
from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import PostsSerializer, EventsSerializer
from .service import toggle_event_rsvp
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .service import toggle_post_like
from django.utils import timezone
from django.db.models import Q

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        data['postedBy'] = user.id
        serializer = PostsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
class ToggleLikePostView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        user = request.user
        post_id = request.data.get("post_id")
        if not post_id:
            return Response({"error": "post_id is required"}, status=400)
        #A View agora apenas "chama" o service e trata os erros
        try: 
            message = toggle_post_like(user=user, post_id=post_id)
            return Response({"message": message}, status=200)
        except ValidationError as e:
            return Response({"error": e.detail}, status=400)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

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

class EventCreateAPIView(generics.CreateAPIView):

        queryset = Events.objects.all()
        serializer_class = EventsSerializer
        permission_classes = [IsAuthenticated]

        @transaction.atomic
        def perform_create(self, serializer):
            serializer.save(postedBy=self.request.user)

class EventListAPIView(generics.ListAPIView):
        queryset = Events.objects.all().order_by('-postedAt')
        serializer_class = EventsSerializer
        permission_classes = [IsAuthenticated]

class EventDetailAPIView(generics.RetrieveAPIView):
        queryset = Events.objects.all()
        serializer_class = EventsSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'pk'
        
class EventUpdateAPIView(generics.UpdateAPIView):
        queryset = Events.objects.all()
        serializer_class = EventsSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'pk'

        def perform_update(self, serializer):
            event = self.get_object()
            if event.postedBy != self.request.user:
                raise PermissionDenied("You do not have permission to edit this event.")
            serializer.save()

class EventDeleteAPIView(generics.DestroyAPIView):
        queryset = Events.objects.all()
        serializer_class = EventsSerializer
        permission_classes = [IsAuthenticated]
        lookup_field = 'pk'

        def perform_destroy(self, instance):
            if instance.postedBy != self.request.user:
                raise PermissionDenied("You do not have permission to delete this event.")
            instance.delete()

class EventRSVPAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk, *args, **kwargs):
        """
        PATCH /events/<pk>/rsvp/  body: {"action": "join"} or {"action": "leave"}
        """
        action = request.data.get("action")
        if action not in ("join", "leave"):
            return Response({"detail": "Action must be 'join' or 'leave'."}, status=status.HTTP_400_BAD_REQUEST)

        # make sure event exists (returns 404 if not)
        event = get_object_or_404(Events, pk=pk)

        try:
            message = toggle_event_rsvp(request.user, str(pk), action)
        except ValidationError as e:
            return Response({"detail": e.detail if hasattr(e, "detail") else str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # return serialized event (with updated total)
        serializer = EventsSerializer(event)
        return Response({"message": message, "event": serializer.data}, status=status.HTTP_200_OK)
