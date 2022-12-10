from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from movie.models import (Movie, MovieComment, MovieCommentLike,
                          MovieCommentDislike, FavoriteMovie, Genre)
from .movie_serializer import (MovieDetailSerializer, MovieListSerializer,
                               MovieLinkSerializer, MovieCommentSerializer,
                               MovieReviewSerializer, GenreSerializer)
from .utils.permissions import CheckUserPermissionToGetMovieLink
from movie.actions import category_action


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


class MovieCommentLikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        comment = get_object_or_404(MovieComment, id=comment_id)
        MovieCommentLike.like(user=request.user, comment=comment)
        return Response(data={"data": 'Ok'}, status=status.HTTP_200_OK)


class MovieCommentDislikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, comment_id):
        comment = get_object_or_404(MovieComment, id=comment_id)
        MovieCommentDislike.dislike(request.user, comment)
        return Response(data={"data": "Ok"}, status=status.HTTP_200_OK)


class AddFavoriteMovieView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        FavoriteMovie.add(request.user, movie)
        return Response(data={"data": 'Ok'}, status=status.HTTP_200_OK)


class GenreListView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieActionView(APIView):
    serializer_classes = MovieListSerializer

    def get(self, request):
        genre_slug = request.query_params.get('genre')
        action = request.query_params.get('action')
        action_info = category_action(action, genre_slug)
        serializer = self.serializer_classes(instance=action_info['queryset'], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
