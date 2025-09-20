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
    
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            user_liking = request.user
            post_id = request.data.get("post_id")
            post_liked = get_object_or_404(Posts, id=post_id)

            already_liked = post_liked.likedBy.filter(id=user_liking.id).exists()

            if already_liked:
                raise ValidationError(f"The user {user_liking.username} already liked this post")

            post_liked.likedBy.add(user_liking)

            post_liked.likes += 1
            post_liked.save()
            return Response(f"The user {user_liking.username} liked this post", status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            user_unliking = request.user
            post_id = request.data.get("post_id")
            post_unliked = get_object_or_404(Posts, id=post_id)

            already_liked = post_unliked.likedBy.filter(id=user_unliking.id).exists()

            if not already_liked:
                raise ValidationError(f"The user {user_unliking.username} didn't like this post")

            post_unliked.likedBy.remove(user_unliking)

            post_unliked.likes -= 1
            post_unliked.save()
            return Response(f"The user {user_unliking.username} unliked this post", status=201)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

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


   # def get_queryset(self):
       # user = self.request.user
    #    posts = Posts.objects.filter(postedBy__in=user.following.all()).order_by('-postedAt')
      #  return posts


