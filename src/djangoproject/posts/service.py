from rest_framework.exceptions import ValidationError
from .models import Posts
from users.models import User 

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