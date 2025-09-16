from rest_framework import serializers
from django.utils import timezone
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from .models import Posts, Event
from users.models import User

class PostsSerializer(serializers.ModelSerializer):
    image = serializers.FileField()
    postedBy = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    likedBy = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=User.objects.all())
    text= serializers.CharField(required=True)

    class Meta:
        model = Posts
        fields = '__all__'

    
    def validate_image(self, image):
        if image.size > 10 * 10 * 1024:
            raise serializers.ValidationError("Very large file. Maximum allowed: 10MB.")
        
        return image

    
    def create(self, validated_data):
        post = Posts.objects.create(image= validated_data['image'],
                                   text=validated_data['text'],
                                   postedBy=validated_data['postedBy']
                                  )
        post.save()
        return post
    

class EventsSerializer(serializers.ModelSerializer):
    # show the id of author and name (we can take this off - but i'll let now guys)
    author_id = serializers.PrimaryKeyRelatedField(source="author", read_only=True)
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)

    class Meta:
        model = Event
        fields = ["id", "title", "event_date", "locate", "author_id", "author_name", "created_at"]
        read_only_fields = ["id", "author_id", "author_name", "created_at"]

    def validate_event_date(self, value):
        # doesn't allow old dates (old than now)
        if value < timezone.now():
            raise serializers.ValidationError("The date/time of the event cannot be earlier than the current time.")
        return value

    def validate_locate(self, value):
        # Pass both (text and url): valides if it is URL, otherwise allows text only
        validator = URLValidator()
        try:
            validator(value)
        except ValidationError:
            # If you want that IT Exist's at least one URL, take of the #:
            # raise serializers.ValidationError("this place needs to be a valid url.")
            pass
        return value

