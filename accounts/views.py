from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout

from .forms import LoginForm, RegisterForm, VerifyAccountForm
from permissions import IsAnonymousHaveOTP, IsAnonymousMixin


class LoginView(IsAnonymousMixin, View):
    template_name = 'accounts/signin.html'
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(data=request.POST, request=request)
        if form.is_valid():
            return redirect(request.GET.get('next', '/'))
        return render(request, self.template_name, {"form": form})


class RegisterView(IsAnonymousMixin, View):
    template_name = 'accounts/signup.html'
    form_class = RegisterForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            return redirect('accounts:verify_account')
        return render(request, self.template_name, {"form": form})


class VerifyAccountView(IsAnonymousHaveOTP, View):
    template_name = 'accounts/verify_account.html'
    form_class = VerifyAccountForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            return redirect(request.session.get('next_url', '/'))
        return render(request, self.template_name, {"form": form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('core:home')


class ForgetPassword(IsAnonymousMixin, TemplateView):
    template_name = 'accounts/forget.html'


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
