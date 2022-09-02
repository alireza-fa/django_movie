from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import ContactUsForm


class HomeView(TemplateView):
    template_name = 'core/home.html'


class PrivacyView(TemplateView):
    template_name = 'core/privacy.html'


class AboutUsView(TemplateView):
    template_name = 'core/about.html'


class ContactUsView(FormView):
    template_name = 'core/contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('core:contact')

    def form_valid(self, form):
        form.save()
        messages.success(request=self.request, message='با تشکر. پیغام شما به دست ما رسید', extra_tags='success')
        return super().form_valid(form)
