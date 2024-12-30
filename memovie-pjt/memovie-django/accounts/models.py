from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre


# Create your models here.
class User(AbstractUser):
    genres = models.ManyToManyField(Genre, related_name='users', blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    aboutMe = models.TextField(null=True)

# class Genre(models.Model):
#     genre_name = models.CharField(max_length=50)