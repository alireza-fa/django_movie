from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Movie
from core.forms import MagazineForm


class MovieView(View):
    template_name = 'movie/movie.html'

    def get(self, request):
        return render(request, self.template_name)


class MovieDetailView(DetailView, FormView):
    model = Movie
    template_name = 'movie/detail.html'
    form_class = MagazineForm
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('movie:detail', args=[self.object.slug])


class MovieFavoriteAction(LoginRequiredMixin, View):
    def get(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)
        favorite = request.user.favorites.filter(movie=movie)
        if favorite.exists():
            favorite.delete()
        else:
            request.user.favorites.create(movie=movie)
        url = reverse_lazy('movie:detail', args=[movie.slug])
        return redirect(request.GET.get('next', url))
