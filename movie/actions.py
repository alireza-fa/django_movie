from django.http import Http404

from movie.models import Movie


def category_action(action):
    if action == 'all':
        return Movie.objects.all().order_by('?')
    if action == 'favorite':
        return Movie.get_all_favorites()
    if action == 'new':
        return Movie.objects.all()
    if action == 'series':
        return Movie.objects.filter(type=2)
    if action == 'film':
        return Movie.objects.filter(type=1)
    return Http404
