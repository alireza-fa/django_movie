# TODO: Movie Comment Like and Dislike
# TODO: Add or Remove From Favorite Movie
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from movie.models import Movie
from .movie_serializer import (MovieDetailSerializer, MovieListSerializer,
                               MovieLinkSerializer, MovieCommentSerializer,
                               MovieReviewSerializer,)
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


class MovieCommentCreateView(APIView):
    serializer_class = MovieCommentSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, movie_id, comment_id=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request, movie_id, comment_id)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class MovieReviewCreateView(APIView):
    serializer_class = MovieReviewSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, movie_id):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request, movie_id)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
