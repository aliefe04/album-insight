from django.urls import path
from . import views

urlpatterns = [
    path('', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('genre/<str:genre_name>/', views.albums_by_genre, name='albums_by_genre'),
]
