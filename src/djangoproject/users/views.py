from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError


class UsersOperationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
        

    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"User deleted succesfully"}, status=204)



class CreateUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)



class ListAllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer = MyTokenObtainPairSerializer

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

class StatusUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        status = {
            "username": user.username,
            "total_followers": user.total_followers,
            "total_following": user.total_following,
        }
        return Response(status)
    
