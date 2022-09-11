from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View, UpdateView, FormView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from permissions import IsRequiredAdminMixin, IsRequiredSuperuserMixin
from core.models import Contact
from .actions import user_action, contact_action
from .forms import UserForm


class DashboardView(IsRequiredAdminMixin, TemplateView):
    template_name = 'panel/dashboard.html'


class UserListView(IsRequiredAdminMixin, ListView):
    model = get_user_model()
    template_name = 'panel/users.html'
    paginate_by = 10

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(*args, object_list=None, **kwargs)
        data['count'] = self.get_queryset().count()
        return data


class UserActionView(IsRequiredAdminMixin, View):

    def get(self, request, pk=0):
        action = request.GET.get('action')
        user_action(request=request, action=action, pk=pk)
        return redirect(request.GET.get('next', 'panel:users'))


class UserEditView(IsRequiredSuperuserMixin, UpdateView):
    template_name = 'panel/edit_user.html'
    model = get_user_model()
    form_class = UserForm
    success_url = reverse_lazy('panel:users')


class ContactListView(IsRequiredAdminMixin, ListView):
    template_name = 'panel/contact.html'
    model = Contact
    queryset = Contact.objects.all().order_by('is_read')
    paginate_by = 10

    def get_context_data(self, *args, object_list=None, **kwargs):
        data = super().get_context_data(*args, object_list=None, **kwargs)
        data['count'] = self.get_queryset().count()
        return data


class ContactActionView(IsRequiredAdminMixin, View):

    def get(self, request, pk=None):
        action = self.request.GET.get('action')
        contact_action(request=request, action=action, pk=pk)
        return redirect('panel:contacts')
