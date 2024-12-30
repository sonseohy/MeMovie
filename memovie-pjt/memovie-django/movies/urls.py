from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list),                    # 전체 영화
    path('<int:movie_pk>/', views.movie_detail),   # 상세 영화
    # path('filter_genre/<int:genre_id>/', views.filter_genre),     # 장르별 영화 필터링
    path('recommend/weather/<str:city_name>/', views.recommend_weather),  # 날씨별 영화 추천
    path('recommend/pastrelease/', views.past_release_today),
    path('recommend/random/', views.recommend_random),
     # 좋아요 API
    path('<int:movie_id>/toggle-like/', views.toggle_like),
    path('<int:actor_id>/toggle-like/actor/', views.toggle_like_actor),
    path('user-likes/movies/', views.user_likes_movie),
    path('user-likes/actors/', views.user_likes_actor),
    # 장르 조회
    path('genres/', views.get_genres),
]

# 테이블 데이터를 기반으로
# 여기서 장르를 조회하는 url을 만들고 그걸 기반으로 view.py 함수를 만들고
# 이걸 vue 에서 axios로 호출해야한다.
# => 장르에 뭐가 있는지 조회하는 함수


# =>
