from django.shortcuts import render
from django.views.generic import View, DetailView

from .models import Movie


class MovieView(View):
    template_name = 'movie/movie.html'

    def get(self, request):
        return render(request, self.template_name)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
