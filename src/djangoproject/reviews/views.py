from rest_framework import generics
from .serializers import ReviewsSerializer
from .models import ReviewTeacher
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from users.models import User 

class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = ReviewTeacher.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def perform_create(self, serializer):
        teacher = get_object_or_404(User, pk=self.kwargs["pk"]) 
        serializer.save(student=self.request.user, teacher=teacher)



class ReviewUpdateAPIView(generics.UpdateAPIView):
    queryset = ReviewTeacher.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_update(self, serializer):
        review = self.get_object()
        if review.student != self.request.user:
            raise PermissionDenied("You do not have permission to edit this review.")
        serializer.save()


class ReviewDeleteAPIView(generics.DestroyAPIView):
    queryset = ReviewTeacher.objects.all()
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"

    def perform_destroy(self, instance):
        if instance.student != self.request.user:
            raise PermissionDenied("You do not have permission to delete this review.")
        instance.delete()


class ReviewListAPIView(generics.ListAPIView):
    queryset = ReviewTeacher.objects.all().order_by("-created_at")
    serializer_class = ReviewsSerializer
    permission_classes = [IsAuthenticated]


class ReviewListUniqueAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewsSerializer

    def get_queryset(self):
        return ReviewTeacher.objects.filter(teacher_id=self.kwargs["pk"])

