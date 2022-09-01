from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.contrib.auth import logout

from .forms import LoginForm, RegisterForm, VerifyAccountForm, ForgetPasswordForm, ForgetPasswordVerifyForm
from permissions import IsAnonymousHaveOTP, IsAnonymousMixin, ForgetPasswordVerifyMixin


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


class ForgetPasswordView(IsAnonymousMixin, View):
    template_name = 'accounts/forget.html'
    form_class = ForgetPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            return redirect('accounts:forget_verify')
        return render(request, self.template_name, {"form": form})


class ForgetPasswordVerifyView(ForgetPasswordVerifyMixin, View):
    template_name = 'accounts/forget_verify.html'
    form_class = ForgetPasswordVerifyForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request=request, data=request.POST)
        if form.is_valid():
            return redirect('accounts:login')
        return render(request, self.template_name, {"form": form})


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'
