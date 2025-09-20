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