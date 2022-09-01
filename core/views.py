from django.shortcuts import render
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = 'core/home.html'


class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'


class AboutUsView(TemplateView):
    template_name = 'core/about.html'


class ContactUsView(TemplateView):
    template_name = 'core/contact.html'
