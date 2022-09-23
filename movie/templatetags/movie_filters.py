from django import template

from movie.models import Movie


register = template.Library()


@register.filter(name='action')
def movie_filtering(action):
    if action == 'new':
        return Movie.objects.all()[:4]
