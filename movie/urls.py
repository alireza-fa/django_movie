from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'movie'

urlpatterns = [
    path('detail/<slug:slug>/', views.MovieDetailView.as_view(), name='detail'),
    path('part_detail/<int:pk>/<slug:slug>/', views.PartDetailSeasonView.as_view(), name='part_detail'),
    path('favorite/<int:pk>/', views.MovieFavoriteAction.as_view(), name='favorite'),
    path('catalogue/', views.MovieCatalogueView.as_view(), name='catalogue'),
    path('category/', views.MovieCategoryView.as_view(), name='category'),
]
