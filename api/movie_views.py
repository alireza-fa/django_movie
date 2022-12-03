# TODO: Detail Movie
# TODO: share Notify
# TODO: Review
# TODO: Comment
# TODO: Movie Comment Like and Dislike
# TODO: Add or Remove From Favorite Movie
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from movie.models import Movie


class MovieListView(ListAPIView):
    queryset = Movie.objects.all()
