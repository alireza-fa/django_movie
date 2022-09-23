from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse

from .choices import TYPE_CHOICES, QUALITY_CHOICES, COUNTRY_CHOICES, GENRE_CHOICES, IRAN, ACTION


class BaseMovieModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(BaseMovieModel):
    name = models.CharField(max_length=120, verbose_name=_('name'))
    english_name = models.CharField(max_length=120, verbose_name=_('english name'))
    slug = models.SlugField(max_length=120, verbose_name=_('slug'))
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

    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        ordering = ('-publish_at',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movie:detail', args=[self.slug])


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='genres', verbose_name=_('genre'))
    genre = models.CharField(max_length=34, choices=GENRE_CHOICES, verbose_name=_('genre'))

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
    # poster = models.ImageField(verbose_name=_('poster'))
    part = models.PositiveSmallIntegerField(verbose_name=_('part'))

    class Meta:
        verbose_name = _('Season Part')
        verbose_name_plural = _('Season Parts')
        ordering = ('part',)

    def __str__(self):
        return f'{self.season} -- part: {self.part}'


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
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))

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
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Movie Review')
        verbose_name_plural = _('Movie Reviews')

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


class MovieCommentDislike(BaseMovieModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='dislikes',
                             verbose_name=_('user'))
    comment = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='dislikes', verbose_name=_('dislike'))

    class Meta:
        verbose_name = _('Movie Comment Dislike')
        verbose_name_plural = _('Movie Comment Dislikes')

    def __str__(self):
        return f'{self.user} - {self.comment}'


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
