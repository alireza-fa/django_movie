from django.contrib import admin
from .models import (FilmMovie, SeriesMovie, FilmLink,
                     SeriesSeason, SeasonPart, PartLink)


class FilmLinkInline(admin.StackedInline):
    model = FilmLink


@admin.register(FilmMovie)
class FilmMovieAdmin(admin.ModelAdmin):
    inlines = (FilmLinkInline,)

    def get_queryset(self, request):
        return self.model.objects.filter(type=1)


@admin.register(SeriesMovie)
class SeriesMovieAdmin(admin.ModelAdmin):
    pass
