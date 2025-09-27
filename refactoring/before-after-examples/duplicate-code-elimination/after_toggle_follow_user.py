##No arquivo views:
class ToggleFollowUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request):
        user = request.user
        target_username = request.data.get("target_username") 

        if not target_username:
            return Response({"error": "target_username is required"}, status=400)

        #A view agora só chama o service e passa os dados
        try:
            message = toggle_user_follow(user=user, target_username=target_username)
            return Response({"message": message}, status=200)
        
        # Trata apenas erros de negócio (que o service levantou ao receber os dados)
        except ValidationError as e:
            return Response({"error": e.detail}, status=400)
        
        except Exception as e:
            return Response({"error": f"An unexpected server error occurred: {str(e)}"}, status=500)
        
        ##No arquivo service:

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