from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db.models import Avg, Sum, Count

from .choices import TYPE_CHOICES, QUALITY_CHOICES, COUNTRY_CHOICES, IRAN
from .managers import IsActiveManager, MovieManager, MovieCommentManager


class BaseMovieModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Genre(models.Model):
    name = models.CharField(max_length=32, verbose_name=_('name'))
    english_name = models.CharField(max_length=32, verbose_name=_('english name'))
    slug = models.SlugField(max_length=40, verbose_name=_('slug'))
    image_cover = models.ImageField(verbose_name=_('image'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/movie/category/?genre={self.slug}'


class Movie(BaseMovieModel):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    english_name = models.CharField(max_length=120, verbose_name=_('english name'))
    slug = models.SlugField(max_length=120, verbose_name=_('slug'), db_index=True)
    description = models.TextField(verbose_name=_('description'))
    poster = models.ImageField(verbose_name='poster', null=True, blank=True)
    image_cover = models.ImageField(verbose_name=_('image cover'))
    image_background = models.ImageField(verbose_name=_('image background'))
    publish_at = models.DateField(verbose_name=_('publish_at'))
    created_at = models.DateField(verbose_name=_('created at'))
    trailer = models.CharField(max_length=240, verbose_name=_('trailer'), null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=1, verbose_name=_('type'))
    quality = models.PositiveSmallIntegerField(choices=QUALITY_CHOICES, default=1, verbose_name=_('quality'))
    time_in_minutes = models.PositiveIntegerField(verbose_name=_('time in minutes'))
    ages = models.PositiveSmallIntegerField(verbose_name=_('ages'))
    is_free = models.BooleanField(default=True, verbose_name=_('is free'))
    country = models.CharField(max_length=34, choices=COUNTRY_CHOICES, verbose_name=_('country'))
    is_active = models.BooleanField(default=True)

    default_manager = models.Manager()
    objects = MovieManager()

    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        ordering = ('-publish_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie:detail', args=[self.slug])

    def get_comments(self):
        return self.comments.filter(is_active=True)

    def get_comment_count(self):
        return self.comments.filter(is_active=True).count()

    def get_reviews(self):
        return self.reviews.filter(is_active=True)

    def get_review_count(self):
        return self.reviews.filter(is_active=True).count()

    def get_avg_rate(self):
        rate = self.reviews.all().aggregate(avg_rate=Avg('rate'))
        if rate['avg_rate']:
            return round(rate['avg_rate'], 1)
        return 8

    @classmethod
    def get_favorites(cls):
        return cls.objects.all().annotate(favorite_count=Count('favorites')).order_by('-favorite_count')[:12]

    @classmethod
    def get_all_favorites(cls):
        return cls.objects.all().annotate(favorite_count=Count('favorites')).order_by('-favorite_count')

    @classmethod
    def get_news(cls):
        return cls.objects.all()[:12]

    @classmethod
    def get_best_rates(cls):
        return cls.default_manager.all().annotate(avg_rate=Sum('reviews__rate')).order_by('-avg_rate')

    @classmethod
    def get_recommend_movie(cls, user):
        genres = user.get_favorite_genres()
        return cls.objects.filter(genres__genre__id__in=genres).distinct()[:5]

    def get_genres(self):
        return self.genres.all()

    def get_similar_movies(self):
        return Movie.objects.filter(genres__genre_id__in=self.genres.all().values('genre__id')).distinct()[:12]


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='genres', verbose_name=_('movie'))
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='movies', verbose_name=_('genre'))

    def __str__(self):
        return f'{self.movie}-{self.genre}'


class FilmMovie(Movie):

    class Meta:
        proxy = True


class SeriesMovie(Movie):
    class Meta:
        proxy = True


class FilmLink(BaseMovieModel):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=120)
    quality = models.IntegerField(verbose_name=_('quality'))
    volume = models.CharField(max_length=32)
    link = models.CharField(max_length=240)

    class Meta:
        verbose_name = _('Film Link')
        verbose_name_plural = _('Film Links')
        ordering = ('-quality',)

    def __str__(self):
        return f'{self.film.name[:32]}---{self.name}'


class FilmSubtitle(models.Model):
    film = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='subtitles', verbose_name=_('film'))
    language = models.CharField(max_length=32, choices=COUNTRY_CHOICES, default=IRAN, verbose_name=_('language'))
    subtitle = models.FileField(max_length=240, verbose_name=_('subtitle'))

    def __str__(self):
        return f'{self.film}-{self.language}'


class SeriesSeason(BaseMovieModel):
    series = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seasons', verbose_name=_('series'))
    season = models.PositiveSmallIntegerField(verbose_name=_('season'))
    name = models.CharField(max_length=120)
    image_background = models.ImageField(verbose_name=_('image background'))

    class Meta:
        verbose_name = _('Series Season')
        verbose_name_plural = _('Series Seasons')
        ordering = ('season',)

    def __str__(self):
        return f'series name: {self.series.name[:32]} -- season: {self.season}'


class SeasonPart(BaseMovieModel):
    season = models.ForeignKey(SeriesSeason, on_delete=models.CASCADE, related_name='parts',
                               verbose_name=_('Season Part'))
    name = models.CharField(max_length=64, verbose_name=_('name'))
    poster = models.ImageField(verbose_name=_('poster'))
    # TODO: below is true and up is false
    # image_cover = models.ImageField(verbose_name=_('image cover'))
    part = models.PositiveSmallIntegerField(verbose_name=_('part'))

    class Meta:
        verbose_name = _('Season Part')
        verbose_name_plural = _('Season Parts')
        ordering = ('part',)

    def __str__(self):
        return f'{self.season} -- part: {self.part}'

    def get_absolute_url(self):
        return reverse('movie:part_detail', args=[self.pk, self.season.series.slug])


class SeasonPartSubtitle(models.Model):
    season_part = models.ForeignKey(SeasonPart,
                                    on_delete=models.CASCADE, related_name='subtitles', verbose_name=_('season part'))
    language = models.CharField(max_length=32, choices=COUNTRY_CHOICES, default=IRAN, verbose_name=_('language'))
    subtitle = models.FileField(max_length=240, verbose_name=_('subtitle'))

    def __str__(self):
        return f'{self.season_part}-{self.language}'


class PartLink(BaseMovieModel):
    season_part = models.ForeignKey(SeasonPart, on_delete=models.CASCADE, related_name='links',
                                    verbose_name=_('part link'))
    name = models.CharField(max_length=64, verbose_name=_('name'))
    quality = models.IntegerField(verbose_name=_('quality'))
    volume = models.CharField(max_length=34)
    link = models.CharField(max_length=240)

    class Meta:
        verbose_name = _('Part Link')
        verbose_name_plural = _('Part Links')
        ordering = ('-quality',)

    def __str__(self):
        return f'{self.season_part} -- quality: {self.quality}'


class MovieComment(BaseMovieModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments',
                             verbose_name=_('user'))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments', verbose_name=_('movie'))
    body = models.TextField(verbose_name=_('body'))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children',
                               verbose_name=_('parent'), null=True, blank=True)
    is_reply = models.BooleanField(default=False, verbose_name=_('is reply'))
    is_read = models.BooleanField(default=False, verbose_name=_('is read'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    default_manager = models.Manager()
    objects = MovieCommentManager()

    class Meta:
        verbose_name = _('Movie Comment')
        verbose_name_plural = _('Movie Comments')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.movie}'


class MovieReview(BaseMovieModel):
    RATE_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='reviews',
                             verbose_name=_('user'))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('movie'))
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, verbose_name=_('rate'))
    subject = models.CharField(max_length=120, verbose_name=_('subject'))
    description = models.TextField(verbose_name=_('body'))
    is_read = models.BooleanField(default=False, verbose_name=_('is read'))
    is_active = models.BooleanField(default=False, verbose_name=_('is active'))

    default_manager = models.Manager()
    objects = IsActiveManager()

    class Meta:
        verbose_name = _('Movie Review')
        verbose_name_plural = _('Movie Reviews')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.movie} - {self.rate}'


class MovieCommentLike(BaseMovieModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='likes',
                             verbose_name=_('user'))
    comment = models.ForeignKey(MovieComment, on_delete=models.CASCADE, related_name='likes', verbose_name=_('comment'))

    class Meta:
        verbose_name = _('Movie Comment Like')
        verbose_name_plural = _('Movie Comment Dislikes')

    def __str__(self):
        return f'{self.user} - {self.comment}'

    @classmethod
    def like(cls, user, comment):
        like_instance = cls.objects.filter(user=user, comment=comment)
        if like_instance.exists():
            like_instance.delete()
        else:
            cls.objects.create(user=user, comment=comment)
        dislike_instance = MovieCommentDislike.objects.filter(user=user, comment=comment)
        if dislike_instance.exists():
            dislike_instance.delete()
        return True


class MovieCommentDislike(BaseMovieModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dislikes',
                             verbose_name=_('user'))
    comment = models.ForeignKey(MovieComment, on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('dislike'))

    class Meta:
        verbose_name = _('Movie Comment Dislike')
        verbose_name_plural = _('Movie Comment Dislikes')

    def __str__(self):
        return f'{self.user} - {self.comment}'

    @classmethod
    def dislike(cls, user, comment):
        dislike_instance = cls.objects.filter(user=user, comment=comment)
        if dislike_instance.exists():
            dislike_instance.delete()
        else:
            cls.objects.create(user=user, comment=comment)
        like_instance = MovieCommentLike.objects.filter(user=user, comment=comment)
        if like_instance.exists():
            like_instance.delete()
        return True


class FavoriteMovie(BaseMovieModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='favorites',
                             verbose_name=_('user'))
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites', verbose_name=_('movie'))

    class Meta:
        verbose_name = _('Favorite Movie')
        verbose_name_plural = _('Favorite Movies')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} - {self.movie}'


class MovieView(BaseMovieModel):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='views', null=True, blank=True)

    class Meta:
        verbose_name = _('Movie View')
        verbose_name_plural = _('Movie Views')

    def __str__(self):
        return f'{self.movie} : {self.user}'


class SliderMovie(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, related_name='slider', verbose_name=_('movie'))
    title = models.CharField(max_length=64, verbose_name=_('title'))
    image = models.ImageField(verbose_name=_('image'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Slider Movie')
        verbose_name_plural = _('Slider Movies')
        ordering = ('-created',)

    def __str__(self):
        return f'{self.movie}'
