from django_filters import rest_framework as filters

from movie.models import Movie


class MovieFilter(filters.FilterSet):
    english_name = filters.CharFilter(field_name='english_name', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ('name', 'english_name', 'publish_at', 'created_at', 'type', 'country')
