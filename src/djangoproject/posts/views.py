
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Posts
from .serializers import PostsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView


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
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    def get_queryset(self):
        user = self.request.user
        posts = Posts.objects.filter(postedBy__in=user.following.all()).order_by('-postedAt')
        return posts
