from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, MyTokenObtainPairSerializer
from .service import toggle_user_follow
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

    def get(self, _request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer = MyTokenObtainPairSerializer


class ToggleFollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        target_username = request.data.get("target_username")

        if not target_username:
            return Response({"error": "target_username is required"}, status=400)

        # A view agora só chama o service e passa os dados
        try:
            message = toggle_user_follow(user=user, target_username=target_username)
            return Response({"message": message}, status=200)

        # Trata apenas erros de negócio (que o service levantou ao receber os dados)
        except ValidationError as e:
            return Response({"error": e.detail}, status=400)

        except Exception as e:
            return Response(
                {"error": f"An unexpected server error occurred: {str(e)}"}, status=500
            )


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
