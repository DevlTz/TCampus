from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import ReviewTeacher
from users.models import User


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
