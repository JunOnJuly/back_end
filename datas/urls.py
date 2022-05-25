from django.urls import path
from . import views

app_name = 'datas'

urlpatterns = [
    # articles
    path('movie/<int:lat>&<int:lon>', views.get_genre_movie),
    path('music/<int:lat>&<int:lon>', views.get_genre_music),
    path('music/recommend/<str:movie_title>', views.recommend_music),
]
