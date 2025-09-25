class ListAllUsersView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)