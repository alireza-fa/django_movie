# TODO: share Notify
# TODO: Review
# TODO: Comment
# TODO: Movie Comment Like and Dislike
# TODO: Add or Remove From Favorite Movie
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from movie.models import Movie
from .movie_serializer import MovieDetailSerializer, MovieListSerializer, MovieLinkSerializer
from .utils.permissions import CheckUserPermissionToGetMovieLink


class MovieDetailView(RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    queryset = Movie.objects.all()


class MovieListView(ListAPIView):
    model = Movie
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


class MovieLinkView(APIView):
    permission_classes = (CheckUserPermissionToGetMovieLink,)
    model = Movie
    serializer_class = MovieLinkSerializer

    def get(self, request, slug):
        movie = get_object_or_404(Movie.objects.all(), slug=slug)
        self.check_object_permissions(request, movie)
        serializer = self.serializer_class(instance=movie)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
