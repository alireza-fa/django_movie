from rest_framework import serializers

from core.models import Magazine, Contact


class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Magazine
        exclude = ('created', 'modified')


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('created', 'is_read')
