from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['id'] = user.id
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,  validators=[validate_password])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    followers = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(required=False, many=True, queryset=User.objects.all())



    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(username= validated_data['username'],
                                   email=validated_data['email'],
                                  )
        user.set_password(validated_data['password'])
        user.save()
        return user
        # é usada em serializers do Django REST Framework para
        # configurar comportamentos específicos de campos, sem precisar reescrevê-los completamente.
