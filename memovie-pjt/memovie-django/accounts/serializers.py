from rest_framework import serializers
from .models import User
from movies.models import Genre

class UserProfileSerializer(serializers.ModelSerializer):
    followings_count = serializers.IntegerField(source='followings.count', read_only=True)
    followers_count = serializers.IntegerField(source='followers.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'followings_count', 'followers_count', 'profile_picture', 'aboutMe', 'genres' ]

class GenersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'
        
class UserUpdateSerializer(serializers.ModelSerializer):
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),  # Genre 모델 쿼리셋
        many=True                      # ManyToMany 관계임을 명시
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'aboutMe', 'genres']  