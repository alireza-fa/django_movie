# TODO: IS FREE and IS NOT FREE Movie
# TODO: share Notify
# TODO: Review
# TODO: Comment
# TODO: Movie Comment Like and Dislike
# TODO: Add or Remove From Favorite Movie
from rest_framework.generics import RetrieveAPIView, ListAPIView

from movie.models import Movie
from .movie_serializer import MovieDetailSerializer, MovieListSerializer


class MovieDetailView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Movie.objects.all()


class MovieListView(ListAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
