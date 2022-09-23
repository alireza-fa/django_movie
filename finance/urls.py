from django.urls import path
from django.views.generic.base import TemplateView


app_name = 'finance'
urlpatterns = [
    path('plan/', TemplateView.as_view(template_name='finance/plan.html'), name='plan'),
]
