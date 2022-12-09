from rest_framework import serializers

from core.models import Magazine


class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        exclude = ('created', 'modified')
