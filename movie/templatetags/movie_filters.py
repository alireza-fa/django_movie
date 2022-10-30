from django import template

from movie.models import Movie, MovieGenre, Genre, SliderMovie


register = template.Library()


@register.filter(name='new_movies')
def new_movies(value):
    return Movie.objects.all()[:4]


@register.filter(name='similar_movies')
def similar_movies(obj):
    movies = MovieGenre.objects.filter(
        genre__in=obj.genres.all().values('genre__id')
    ).exclude(movie=obj).order_by('?')[:12]
    return movies


@register.filter(name='favorite_movies')
def favorite_movies(value):
    return Movie.get_favorites()


@register.filter(name='new_movies')
def new_movies(value):
    return Movie.get_news()[:12]


@register.filter(name='genre_movies')
def genre_movies(value):
    return Genre.objects.all()


@register.filter(name='random_movies')
def random_movies(value):
    return Movie.objects.all().order_by('?')[:12]


@register.filter(name='series_movies')
def series_movies(value):
    return Movie.objects.filter(type=2).order_by('?')[:12]


@register.filter(name='slider_movies')
def slider_movies(value):
    return SliderMovie.objects.all()[:8]
