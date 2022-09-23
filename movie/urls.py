from django.urls import path
from django.views.generic import TemplateView

from . import views


app_name = 'movie'

urlpatterns = [
    path('detail/<slug:slug>/', views.MovieDetailView.as_view(), name='detail'),
    path('favorite/<int:pk>/', views.MovieFavoriteAction.as_view(), name='favorite'),
    path('category/', TemplateView.as_view(template_name='movie/category.html')),
    path('catalogue/', TemplateView.as_view(template_name='movie/catalogue.html'), name='catalogue')
]
