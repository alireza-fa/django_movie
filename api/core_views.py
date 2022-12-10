from rest_framework.generics import CreateAPIView

from .core_serializers import MagazineSerializer, ContactUsSerializer
from core.models import Magazine


class MagazineCreateView(CreateAPIView):
    model = Magazine
    serializer_class = MagazineSerializer


class ContactUsCreateSerializer(CreateAPIView):
    serializer_class = ContactUsSerializer
