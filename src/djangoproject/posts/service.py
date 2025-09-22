from rest_framework.exceptions import ValidationError
from .models import Posts, Events
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

def get_all_posts():
    return Posts.objects.all().order_by("-postedAt")
def get_post_by_id(post_id: str):
    try:
        return Posts.objects.get(id=post_id)
    except Posts.DoesNotExist:
        raise ValidationError(f"Post with id {post_id} not found")
def get_posts_by_user(user: User):
    return Posts.objects.filter(postedBy=user).order_by("-postedAt")
def create_post(user: User, image, text: str):
    post = Posts.objects.create(image=image, text=text, postedBy=user)
    post.save()
    return post
def toggle_event_rsvp(user: User, event_id: str, action: str):
    """
    Toggle RSVP for the event. `action` must be 'join' or 'leave'.
    Raises ValidationError on invalid operations (double join, leaving when not joined).
    Returns a human-friendly message on success.
    """
    try:
        event = Events.objects.get(id=event_id)
    except Events.DoesNotExist:
        raise ValidationError(f"Event with id {event_id} not found")

    if action not in ("join", "leave"):
        raise ValidationError("Action must be 'join' or 'leave'")

    already_joined = event.participants.filter(id=user.id).exists()

    if action == "join":
        if already_joined:
            raise ValidationError("User already confirmed attendance.")
        event.participants.add(user)
        # increment participants_count atomically-ish (simple approach consistent with repo style)
        event.participants_count = (event.participants_count or 0) + 1
        event.save()
        return f"The user {user.username} joined this event"
    else:  # leave
        if not already_joined:
            raise ValidationError("User is not confirmed for this event.")
        event.participants.remove(user)
        # ensure no negative counters
        event.participants_count = max((event.participants_count or 0) - 1, 0)
        event.save()
        return f"The user {user.username} left this event"
