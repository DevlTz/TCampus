from rest_framework.exceptions import ValidationError
from .models import Posts
from users.models import User 

##Service:

def toggle_post_like(user: User, post_id: str):
   
    try:
        post = Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        raise ValidationError(f"Post with id {post_id} not found")

    already_liked = post.likedBy.filter(id=user.id).exists()

    if already_liked:
        post.likedBy.remove(user)
        post.likes -= 1
        action_message = "unliked"
    else:
        post.likedBy.add(user)
        post.likes += 1
        action_message = "liked"
    
    post.save()
    
    return f"The user {user.username} {action_message} this post"

##View:
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