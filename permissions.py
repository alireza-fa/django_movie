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
