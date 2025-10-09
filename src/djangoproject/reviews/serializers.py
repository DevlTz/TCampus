from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import ReviewTeacher
from users.models import User
from django.db.models import Avg


class ReviewsSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    student = serializers.PrimaryKeyRelatedField(
        required=True, queryset=User.objects.all()
    )
    score = serializers.IntegerField(required=True)

    class Meta:
        model = ReviewTeacher
        fields = "__all__"

    def create(self, validated_data):
        review = ReviewTeacher.objects.create(
            score=validated_data["score"],
            teacher=validated_data["teacher"],
            student=validated_data["student"],
        )
        review.save()
        return review
    
class TeacherDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'reviews', 'average_score']

    def get_average_score(self, obj):
        return obj.reviews.aggregate(avg=Avg('score'))['avg']