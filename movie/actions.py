from django.http import Http404
from django.shortcuts import get_object_or_404

from movie.models import Movie, Genre


def _get_all_movies():
    return Movie.objects.all().order_by('?')


def _get_favorite_movies():
    return Movie.get_all_favorites()


def _get_new_movies():
    return Movie.objects.all()


def _get_series_movies():
    return Movie.objects.filter(type=2)


def _get_film_movies():
    return Movie.objects.filter(type=1)


def category_action(action=None, genre=None):
    movie_action = {
        "all": _get_all_movies,
        "favorite": _get_favorite_movies,
        "new": _get_new_movies,
        "series": _get_series_movies,
        "film": _get_film_movies,
    }

    queryset = dict()

    if genre:
        genre = get_object_or_404(Genre, slug=genre)

    if action and action in movie_action:
        queryset['queryset'] = movie_action[action]()
        if genre:
            queryset['category'] = genre.name
            queryset['queryset'] = queryset['queryset'].filter(genres__genre=genre)
            return queryset
        queryset['category'] = action
        return queryset

    if genre:
        queryset['category'] = genre.name
        queryset['queryset'] = Movie.objects.filter(genres__genre=genre)
        return queryset

    return Http404
