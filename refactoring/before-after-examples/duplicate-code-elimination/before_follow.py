class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request):
        try:
            user_following = request.user
            target_username = request.data.get("user_to_follow")
            user_to_follow = get_object_or_404(User, username=target_username)

            exists = user_following.following.filter(id=user_to_follow.id).exists()

            if exists:
                raise ValidationError(f"The user {user_following.username} is already following {target_username}")
            
            if user_following.username == user_to_follow.username:
                raise ValidationError("Following yourself is not allowed")
        

            user_following.following.add(user_to_follow)
            user_to_follow.followers.add(user_following)


            user_following.total_following += 1
            user_to_follow.total_followers += 1
            user_following.save()
            user_to_follow.save()


            return Response(f"The user {user_following.username} is following {target_username}", status= 200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
