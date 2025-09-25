class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            
            user_unfollowing = request.user
            target_username = request.data.get("user_to_unfollow")
            user_to_unfollow = get_object_or_404(User, username=target_username)

            exists = user_unfollowing.following.filter(id=user_to_unfollow.id).exists()

            if not exists:
                raise ValidationError(f"The user {user_unfollowing.username} doesn't follow {target_username}")
            
            if user_unfollowing.username == user_to_unfollow.username:
                raise ValidationError("Unfollowing yourself is not allowed")

            user_unfollowing.following.remove(user_to_unfollow)
            user_to_unfollow.following.remove(user_unfollowing)

            user_unfollowing.total_following -= 1
            user_to_unfollow.total_followers -= 1
            user_unfollowing.save()
            user_to_unfollow.save()
 
            return Response(f"The user {user_unfollowing.username} unfollowed {target_username}", status= 200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)