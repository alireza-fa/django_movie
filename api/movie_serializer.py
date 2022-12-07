from rest_framework import serializers

from movie.models import Movie, MovieComment, MovieReview, MovieGenre, Genre


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
        exclude = ('modified', 'is_active', 'is_read')

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


class MovieDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(method_name='get_comments', read_only=True)
    reviews = serializers.SerializerMethodField(method_name='get_reviews', read_only=True)
    avg_rate = serializers.SerializerMethodField(method_name='get_avg_rate', read_only=True)
    genres = serializers.SerializerMethodField(method_name='get_genres', read_only=True)

    class Meta:
        model = Movie
        exclude = ('is_active', 'created', 'modified')

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
