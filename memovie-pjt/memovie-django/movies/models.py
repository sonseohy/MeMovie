from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    genre_name = models.CharField(max_length=50)

class Actor(models.Model):
    actor_name = models.CharField(max_length=100)
    actor_profile_img = models.CharField(max_length=255)

class Movie(models.Model):
    title = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()
    # 영화 상영 시간 (분 단위)
    runtime = models.IntegerField()  # 예: 120 (120분)
    # 영화 포스터 이미지 URL
    poster_url = models.URLField()
    # 영화 태그라인
    tagline = models.CharField(max_length=255, blank=True, null=True)
    # 영화 감독
    director = models.CharField(max_length=255)
    # 영화 평점
    vote_average = models.FloatField(default=0.0)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

# 영화 좋아요
class MovieLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # 같은 영화에 대해 중복 좋아요 방지

# 배우 좋아요
class ActorLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'actor')  # 같은 영화에 대해 중복 좋아요 방지