from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.http import Http404

from movie.models import (Movie, MovieComment, MovieReview, MovieGenre,
                          Genre, FilmLink, FilmSubtitle, SeriesSeason, SeasonPart, PartLink, SeasonPartSubtitle)


class MovieCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieComment
        exclude = ('modified', 'is_active', 'is_read', 'id')
        extra_kwargs = {
            "user": {"read_only": True},
            "movie": {"read_only": True},
            "parent": {"read_only": True},
            "is_reply": {"read_only": True}
        }

    def save(self, request, movie_id, comment_id=None):
        movie = get_object_or_404(Movie, id=movie_id)
        comment = MovieComment(
            user=request.user, movie=movie, body=self.validated_data['body']
        )
        if comment_id:
            parent_comment = get_object_or_404(MovieComment, id=comment_id)
            if not parent_comment.movie == movie:
                raise Http404
            comment.parent = parent_comment
            comment.is_reply = True
        comment.save()
        return comment


class MovieCommentChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieComment
        fields = ('user', 'movie', 'body', 'parent', 'is_reply', 'created')


class MovieCommentParentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(method_name='get_children', read_only=True)
    like = serializers.SerializerMethodField(method_name='get_like_count', read_only=True)
    dislike = serializers.SerializerMethodField(method_name='get_dislike_count', read_only=True)

    class Meta:
        model = MovieComment
        exclude = ('modified', 'is_active', 'is_read', 'id')

    def get_children(self, obj):
        comments = obj.children.filter(parent=obj)
        return MovieCommentChildSerializer(instance=comments, many=True).data

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()


class MovieReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview
        exclude = ('is_read', 'is_active', 'modified')
        extra_kwargs = {
            "user": {"read_only": True},
            "movie": {"read_only": True},
            "created": {"read_only": True}
        }

    def save(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        data = self.validated_data
        MovieReview.objects.create(
            user=request.user, movie=movie, rate=data['rate'],
            subject=data['subject'], description=data['description']
        )
        return True


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieGenreSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField(method_name='get_genre', read_only=True)

    def get_genre(self, obj):
        return GenreSerializer(instance=obj.genre).data

    class Meta:
        model = MovieGenre
        fields = ('movie', 'genre')


class MovieListSerializer(serializers.ModelSerializer):
    avg_rate = serializers.SerializerMethodField(method_name='get_avg_rate', read_only=True)
    genres = serializers.SerializerMethodField(method_name='get_genres', read_only=True)

    class Meta:
        model = Movie
        exclude = ('description', 'image_background', 'trailer', 'created', 'modified', 'poster')

    def get_genres(self, obj):
        genres = obj.get_genres()
        return MovieGenreSerializer(instance=genres, many=True).data

    def get_avg_rate(self, obj):
        return obj.get_avg_rate()


class MovieDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)
    avg_rate = serializers.SerializerMethodField(method_name='get_avg_rate', read_only=True)
    genres = serializers.SerializerMethodField(method_name='get_genres', read_only=True)
    similar_movies = serializers.SerializerMethodField(method_name='get_similar_movies', read_only=True)

    class Meta:
        model = Movie
        exclude = ('is_active', 'created', 'modified')

    def get_similar_movies(self, obj):
        movies = obj.get_similar_movies()
        return MovieListSerializer(instance=movies, many=True).data

    def get_genres(self, obj):
        genres = obj.get_genres()
        return MovieGenreSerializer(instance=genres, many=True).data

    def get_avg_rate(self, obj):
        return obj.get_avg_rate()

    def get_reviews(self, obj):
        reviews = obj.reviews.all()
        return MovieReviewSerializer(instance=reviews, many=True).data

    def get_comments(self, obj):
        comments = obj.comments.filter(movie=obj, is_reply=False)
        serializer = MovieCommentParentSerializer(instance=comments, many=True)
        return serializer.data


class FilmSubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmSubtitle
        exclude = ('film',)


class FilmLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmLink
        exclude = ('created', 'modified', 'id')


class PartLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartLink
        exclude = ('season_part', 'created', 'modified', 'id')


class SeasonPartSubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonPartSubtitle
        exclude = ('season_part',)


class SeasonPartSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField(method_name='get_links', read_only=True)
    subtitles = serializers.SerializerMethodField(method_name='get_subtitles', read_only=True)

    class Meta:
        model = SeasonPart
        exclude = ('season', 'id', 'created', 'modified')

    def get_subtitles(self, obj):
        subtitles = obj.subtitles.all()
        return SeasonPartSubtitleSerializer(instance=subtitles, many=True).data

    def get_links(self, obj):
        parts = obj.links.all()
        return PartLinkSerializer(instance=parts, many=True).data


class SeriesSeasonSerializer(serializers.ModelSerializer):
    parts = serializers.SerializerMethodField(method_name='get_parts', read_only=True)

    class Meta:
        model = SeriesSeason
        exclude = ('created', 'modified', 'id')

    def get_parts(self, obj):
        parts = obj.parts.all()
        return SeasonPartSerializer(instance=parts, many=True).data


class MovieLinkSerializer(serializers.Serializer):
    links = serializers.SerializerMethodField(method_name='get_links', read_only=True)
    subtitles = serializers.SerializerMethodField(method_name='get_subtitles', read_only=True)

    def get_links(self, obj):
        if obj.type == 1:
            instances = obj.links.all()
            return FilmLinkSerializer(instance=instances, many=True).data
        seasons = obj.seasons.all()
        return SeriesSeasonSerializer(instance=seasons, many=True).data

    def get_subtitles(self, obj):
        subtitles = obj.subtitles.all()
        return FilmSubtitleSerializer(instance=subtitles, many=True).data
