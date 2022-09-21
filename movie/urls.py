from django.urls import path

from . import views


app_name = 'movie'

urlpatterns = [
    path('detail/<slug:slug>/', views.MovieDetailView.as_view(), name='detail'),
    path('movie/favorite/<int:pk>/', views.MovieFavoriteAction.as_view(), name='favorite'),
]
