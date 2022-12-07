# TODO: share Notify
# TODO: Review
# TODO: Comment
# TODO: Movie Comment Like and Dislike
# TODO: Add or Remove From Favorite Movie
from rest_framework.generics import RetrieveAPIView

from movie.models import Movie
from .movie_serializer import MovieDetailSerializer


class MovieDetailView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Movie.objects.all()
