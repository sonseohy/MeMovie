from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list),                      # 전체 게시글 목록
    path('<int:article_pk>/', views.article_detail),   # 상세 게시글 조회, 수정, 삭제
    path('<int:article_pk>/comments/', views.comment),   # 전체 댓글 조회 및 댓글 생성
    path('<int:article_pk>/like/', views.like), # 게시글 좋아요
]
