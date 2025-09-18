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
