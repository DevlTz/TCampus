from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Posts, Events
from .validator import validate_image_size
from users.models import User


class PostsSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False, validators=[validate_image_size])
    postedBy = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    likedBy = serializers.PrimaryKeyRelatedField(
        required=False, many=True, queryset=User.objects.all()
    )
    text = serializers.CharField(required=True)

    class Meta:
        model = Posts
        fields = "__all__"

    
    def create(self, validated_data):
        post = Posts.objects.create(
            image=validated_data.get("image"),
            text=validated_data["text"],
            postedBy=validated_data["postedBy"],
        )
        return post
    
    def validate(self, data):
        if not data.get("text") and not data.get("image"):
            raise serializers.ValidationError(
                "The post must contain at least a text or a image"
            )
        return data


class EventsSerializer(serializers.ModelSerializer):
    # show the id of author and name (we can take this off - but i'll let now guys)
    postedBy_id = serializers.PrimaryKeyRelatedField(source="postedBy", read_only=True)
    postedBy_username = serializers.CharField(
        source="postedBy.get_full_name", read_only=True
    )
    event_date = serializers.DateTimeField(required=True)
    total_participants = serializers.IntegerField(
        source="total_participants", read_only=True
    )

    class Meta:
        model = Events
        fields = [
            "id",
            "title",
            "event_date",
            "locate",
            "postedBy_id",
            "postedBy_username",
            "postedAt",
            "total_participants",
        ]
        read_only_fields = [
            "id",
            "postedBy_id",
            "postedBy_username",
            "postedAt",
            "total_participants",
        ]

    def validate_event_date(self, value):
        # doesn't allow old dates (old than now)
        if value < timezone.now():
            raise serializers.ValidationError(
                "The date/time of the event cannot be earlier than the current time."
            )
        return value

    def validate_locate(self, value):
        # Pass both (text and url): validates if it's URL, otherwise allows text only
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            # If you want that IT Exist's at least one URL, take of the #:
            # raise serializers.ValidationError("this place needs to be a valid url.")
            pass
        return value
