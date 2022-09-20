from django.contrib import admin
from .models import (FilmMovie, SeriesMovie, FilmLink, SeriesSeason,
                     SeasonPart, PartLink, FilmSubtitle, SeasonPartSubtitle, MovieGenre)


class MovieGenreInline(admin.StackedInline):
    model = MovieGenre
    extra = 1


class FilmLinkInline(admin.StackedInline):
    model = FilmLink


class FilmSubtitleInline(admin.StackedInline):
    model = FilmSubtitle


@admin.register(FilmMovie)
class FilmMovieAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('english_name',)}
    inlines = (FilmLinkInline, FilmSubtitleInline, MovieGenreInline)

    def get_queryset(self, request):
        return self.model.objects.filter(type=1)


class SeriesSeasonInline(admin.StackedInline):
    model = SeriesSeason


@admin.register(SeriesMovie)
class SeriesMovieAdmin(admin.ModelAdmin):
    inlines = (SeriesSeasonInline, MovieGenreInline)

    def get_queryset(self, request):
        return self.model.objects.filter(type=2)


class SeasonPartInline(admin.StackedInline):
    model = SeasonPart


@admin.register(SeriesSeason)
class SeriesSeasonAdmin(admin.ModelAdmin):
    inlines = (SeasonPartInline,)


class PartLinkInline(admin.StackedInline):
    model = PartLink


class SeasonPartSubtitleInline(admin.StackedInline):
    model = SeasonPartSubtitle


@admin.register(SeasonPart)
class SeasonPartAdmin(admin.ModelAdmin):
    inlines = (PartLinkInline, SeasonPartSubtitleInline)
