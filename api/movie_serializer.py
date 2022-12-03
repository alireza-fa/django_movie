from rest_framework import serializers

from movie.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ('is_active', 'created', 'modified')
