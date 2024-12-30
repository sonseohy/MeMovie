from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:username>/', views.profile),
    # path('profile/<str:username>/upload/', views.upload_profile_image, name='upload_profile_image'),  # 프로필 이미지 업로드
    path('<int:user_pk>/follow/', views.follow),
]