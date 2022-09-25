from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import View, DetailView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Movie, MovieComment, MovieReview, SeasonPart, Genre
from core.forms import MagazineForm
from .forms import CommentMovieForm, ReviewMovieForm
from .actions import category_action


class MovieView(View):
    template_name = 'movie/movie.html'

    def get(self, request):
        return render(request, self.template_name)


class MovieDetailView(DetailView, FormView):
    model = Movie
    template_name = 'movie/detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_form_class(self):
        form_class = self.request.POST.get('form_class')
        if self.request.user.is_authenticated:
            if form_class == 'comment':
                return CommentMovieForm
            elif form_class == 'review':
                return ReviewMovieForm
        return MagazineForm

    def get_success_url(self):
        return self.request.path

    def form_invalid(self, form):
        return render(self.request, self.template_name, {"object": self.get_object(), "form": form})

    def form_valid(self, form):
        form_class = self.get_form_class()
        if form_class == CommentMovieForm:
            MovieComment.objects.create(user=self.request.user, movie=self.get_object(), body=form.cleaned_data['body'])
        elif form_class == ReviewMovieForm:
            cd = form.cleaned_data
            MovieReview.objects.create(user=self.request.user, movie=self.get_object(),
                                       rate=cd['rate'], subject=cd['subject'], description=cd['description'])
        else:
            form.save()
        return super().form_valid(form)


class PartDetailSeasonView(MovieDetailView):
    template_name = 'movie/part_detail.html'

    def get_context_data(self, **kwargs):
        part = get_object_or_404(SeasonPart, pk=self.kwargs['pk'])
        obj = get_object_or_404(Movie, slug=self.kwargs['slug'])
        return {
            "part": part,
            "object": obj
        }

    def get_object(self, queryset=None):
        return get_object_or_404(Movie, slug=self.kwargs['slug'])

    def form_invalid(self, form):
        context = self.get_context_data()
        return render(self.request, self.template_name,
                      {"form": form,
                       "part": context['part'],
                       "object": context['object']}
                      )


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


class MovieCatalogueView(ListView):
    model = Genre
    template_name = 'movie/catalogue.html'
    queryset = Genre.objects.all()


class MovieCategoryView(ListView):
    model = Movie
    template_name = 'movie/category.html'
    paginate_by = 20

    def get_queryset(self):
        genre = self.request.GET.get('genre')
        action = self.request.GET.get('action')
        if genre:
            genre = get_object_or_404(Genre, slug=genre)
            self.category = genre.name
            return Movie.objects.filter(genres__genre=genre)
        if action:
            self.category = action
            return category_action(action)
        raise Http404

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        context['category'] = self.category
        return context
