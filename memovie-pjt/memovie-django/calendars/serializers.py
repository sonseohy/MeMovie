from rest_framework import serializers
from .models import Calendar, Movie
from django.contrib.auth import get_user_model

class CalendarListSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # read_only 설정
    # movie_id를 PrimaryKey로 처리
    movie = serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all())
    # created_at 필드에서 시간은 제외하고 날짜만 반환

    class Meta:
        model = Calendar
        fields = '__all__'
        read_only_fields = ['user']

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'