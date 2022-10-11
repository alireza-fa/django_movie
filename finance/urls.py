from django.urls import path
from django.views.generic.base import TemplateView

from . import views


app_name = 'finance'
urlpatterns = [
    path('plan/', TemplateView.as_view(template_name='finance/plan.html'), name='plan'),
    path('plan/pay/', views.PlanPayView.as_view(), name='pay_plan'),
    path('plan/verify/', views.PlanPayVerify.as_view(), name='pay_verify'),
]
