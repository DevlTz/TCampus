from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from .models import User

def toggle_user_follow(user: User, target_username: str):
    
    if user.username == target_username:
        raise ValidationError("Following yourself is not allowed.")
    try:
        user_to_follow = User.objects.get(username=target_username)
    except User.DoesNotExist:
        raise ValidationError(f"User '{target_username}' not found.")
    
    #Garante a lógica do Toggle
    already_following = user.following.filter(id=user_to_follow.id).exists()

    if already_following:
        # Unfollow
        user.following.remove(user_to_follow)
        user_to_follow.followers.remove(user)
        user.total_following -= 1
        user_to_follow.total_followers -= 1
        action_message = "unfollowed"
    else:
        #Follow
        user.following.add(user_to_follow)
        user_to_follow.followers.add(user) 
        user.total_following += 1
        user_to_follow.total_followers += 1
        action_message = "followed"

    user.save()
    user_to_follow.save()

    return f"The user {user.username} {action_message} {target_username}"