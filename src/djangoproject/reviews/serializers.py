from rest_framework import serializers
from .models import ReviewTeacher
from users.models import User
from django.db.models import Avg


class ReviewsSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)    
    score = serializers.IntegerField(required=True, min_value=1, max_value=10)

    class Meta:
        model = ReviewTeacher
        fields = "__all__"

    def create(self, validated_data):
        review = ReviewTeacher.objects.create(
            score=validated_data["score"],
            teacher=validated_data["teacher"],
            student=validated_data["student"],
            comment=validated_data.get("comment", "")
        )
        return review
    
class TeacherDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewsSerializer(many=True, read_only=True, source='reviews_received')
    average_score = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'reviews', 'average_score']

    def get_average_score(self, obj):
        return obj.reviews_received.aggregate(avg=Avg('score'))['avg']