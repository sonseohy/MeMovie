from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar_list),
    path('<int:calendar_pk>/', views.calendar_detail),
]

