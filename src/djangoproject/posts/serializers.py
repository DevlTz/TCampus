from rest_framework import serializers
from .models import Posts
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
            raise serializers.ValidationError("Arquivo muito grande. Máximo permitido: 10MB.")
        
        return image

    
    def create(self, validated_data):
        post = Posts.objects.create(image= validated_data['image'],
                                   text=validated_data['text'],
                                   postedBy=validated_data['postedBy']
                                  )
        post.save()
        return post
    
