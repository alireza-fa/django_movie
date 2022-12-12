from rest_framework.generics import ListAPIView

from .finance_serializer import PlanSerializer
from finance.models import Plan


class PlanListView(ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
