from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Posts, Events
from django.db import transaction
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError
from .serializers import PostsSerializer, EventsSerializer
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
    
   # Combined feed: posts + events. By default shows posts+events from followed users.
   #  If ?events_scope=all is present, events will include upcoming events from ALL users
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        #
        # POSTS: we want posts from followed users only
        posts_qs = Posts.objects.filter(postedBy__in=user.following.all()).order_by('-postedAt')
        posts_data = PostsSerializer(posts_qs, many=True, context={"request": request}).data

        # EVENTS: can be filtered by scope
        # ?events_scope=all  -> include events from any user
        # Anything else (default) -> include events from followed users only
        scope = request.query_params.get('events_scope', 'following')
        now = timezone.now()

        if scope == 'all':
            # Include only upcoming events from all users
            events_qs = Events.objects.filter(event_date__gte=now).order_by('-event_date')
        else:
            # Default: include events from followed users only
            # Can include past events too (e.g., from yesterday)
            events_qs = Events.objects.filter(postedBy__in=user.following.all()).order_by('-event_date')

        events_data = EventsSerializer(events_qs, many=True, context={"request": request}).data

        # Now we have two lists of dicts: posts_data and events_data
        # We need to merge them into a single feed, sorted by date (most recent first)
        normalized = []
        # adding posts to normalized list
        for p in posts_data:
            normalized.append({
                "type": "post",
                "sort_date": p.get("postedAt") or p.get("created_at"),
                "data": p
            })
            # adding events to normalized list
        for e in events_data:
            normalized.append({
                "type": "event",
                "sort_date": e.get("event_date"),
                "data": e
            })

        normalized.sort(key=lambda x: x["sort_date"] or "", reverse=True)
        # constructing final feed
        feed = []
        for item in normalized:
            obj = dict(item["data"])
            obj["type"] = item["type"]
            feed.append(obj)

        # return combined feed. 
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

