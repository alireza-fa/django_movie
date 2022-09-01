from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, ListView, View
from django.contrib.auth import get_user_model

from permissions import IsRequiredAdminMixin


class DashboardView(IsRequiredAdminMixin, TemplateView):
    template_name = 'panel/dashboard.html'


class UserListView(IsRequiredAdminMixin, ListView):
    model = get_user_model()
    template_name = 'panel/users.html'
    paginate_by = 10


class ChangeUserStatusView(IsRequiredAdminMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        bool_active = user.is_active
        if bool_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect(request.GET.get('next', 'panel:users'))


class UserDeleteView(IsRequiredAdminMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(get_user_model(), id=user_id)
        user.delete()
        return redirect(request.GET.get('next', 'panel:users'))


class UserEditView(IsRequiredAdminMixin, TemplateView):
    template_name = 'panel/edit_user.html'

