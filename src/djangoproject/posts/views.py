
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Posts
from .serializers import PostsSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from .service import toggle_post_like

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
    permission_classes = [IsAuthenticated]
    serializer_class = PostsSerializer
    def get_queryset(self):
        user = self.request.user
        posts = Posts.objects.filter(postedBy__in=user.following.all()).order_by('-postedAt')
        return posts
