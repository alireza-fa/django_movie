from django.http import Http404
from django.shortcuts import redirect
from django.core.cache import cache


class IsAnonymousHaveOTP:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        register_info = request.session.get('register_info')
        if not register_info:
            return redirect('accounts:register')
        cache_info = cache.get(key=register_info.get('username'))
        if not cache_info:
            return redirect('accounts:register')
        return super().dispatch(request, *args, **kwargs)


class IsAnonymousMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)


class ForgetPasswordVerifyMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('code:home')
        forget_info = request.session.get('forget_info')
        if not forget_info:
            return redirect('accounts:forget')
        cache_info = cache.get(key=forget_info.get('email'))
        if not cache_info:
            return redirect('accounts:forget')
        return super().dispatch(request, *args, **kwargs)


class IsRequiredAdminMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_staff:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class IsRequiredSuperuserMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        if not request.user.is_superuser:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class PostRequiredLogin:
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if not request.user.is_authenticated:
                raise Http404
        return super().dispatch(request, *args, **kwargs)
