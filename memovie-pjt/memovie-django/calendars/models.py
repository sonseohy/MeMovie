from django.db import models
from movies.models import Movie
from django.conf import settings

# Create your models here.
class Calendar(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)  # 영화 제목
    content = models.TextField()              # 영화 내용
    rating = models.IntegerField()            # 별점 (1~5)
    poster_url = models.CharField(max_length=1024, blank=True, null=True)  # 포스터 이미지 URL
    created_date = models.DateField()