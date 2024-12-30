from rest_framework import serializers
from .models import Movie, Genre, Actor

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField()
    release_date = serializers.DateField()
    genres = serializers.SerializerMethodField()
    vote_average = serializers.FloatField()
    popularity = serializers.FloatField()
    runtime = serializers.IntegerField()
    tagline = serializers.CharField()
    poster_url = serializers.SerializerMethodField()

    # 장르 이름만 추출
    def get_genres(self, obj):
        return [genre.get("name") for genre in obj.get("genres", [])]

    # 포스터 URL 생성
    def get_poster_url(self, obj):
        poster_path = obj.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return None

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'