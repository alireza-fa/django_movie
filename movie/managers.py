from django.db.models import Manager


class IsActiveManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class MovieManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'genres', 'comments', 'reviews', 'favorites', 'views').filter(is_active=True)


class MovieCommentManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'movie', 'user').prefetch_related('dislikes', 'likes').filter(is_active=True)


class MovieReviewManager(Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('movie').filter(is_active=True)
