from django.urls import path

from . import views


app_name = 'core'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('about-us/', views.AboutUsView.as_view(), name='about'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact'),
]
