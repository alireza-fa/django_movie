from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.cache import cache
from django.shortcuts import redirect

from .utils import otp_code
from .tasks import send_mail_task
from utils.convert_numbers import persian_to_english
from random import randint


error_msg = {
    "invalid": 'مقدار وارد شده معتبر نمی باشد',
    "required": 'این فیلد نمی تواند خالی باشد'
}


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'sign__input', "placeholder": 'ایمیل / نام کاربری'}),
        error_messages=error_msg,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'sign__input', "placeholder": 'رمز عبور'}),
        error_messages=error_msg,
    )
    remember = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"id": 'remember', "name": 'remember', "checked": 'checked'})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        data = self.cleaned_data
        if data.get('email') and data.get('password'):
            user = authenticate(username=data['email'], password=data['password'])
            if user is None:
                raise forms.ValidationError('کاربری با این مشخصات پیدا نشد')
            login(request=self.request, user=user)
            if not data.get('remember'):
                self.request.session.set_expiry(0)
        return data


class RegisterForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'sign__input', "placeholder": 'نام کاربری'}),
        max_length=32, error_messages=error_msg
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": 'sign__input', "placeholder": 'ایمیل'}),
        max_length=199, error_messages=error_msg
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": 'sign__input', "placeholder": 'رمز عبور'}),
        max_length=64, error_messages=error_msg
    )
    privacy_check = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={"id": 'privacy', "name": 'privacy', "checked": 'checked'}),
        required=True, error_messages=error_msg
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError('کاربری با این نام کاربری وجود دارد')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('کاربری با این ایمیل وجود دارد')
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError('کلمه عبور نمی تواند از ۸ حرف کوچک تر باشد')
        return password

    def clean(self):
        data = self.cleaned_data

        if data.get('email') and data.get('username') and data.get('password'):
            email_time = cache.get(key=data['email'])
            if not email_time:
                cache.set(key=data['email'], value=1, timeout=86400)
            else:
                if email_time >= 10:
                    raise forms.ValidationError('شما بیشتر از حد مجاز تلاش کرده اید. ۲۴ ساعت بعد دوباره امتحان کنید')
                else:
                    cache.incr(key=data['email'])

            self.request.session['register_info'] = {
                "username": data['username'], "email": data['email'], "password": data['password']
            }
            has_otp_code = cache.get(key=data['username'])
            if not has_otp_code:
                code = otp_code()
                cache.set(
                    key=data['username'], timeout=120,
                    value={"email": data['email'],
                           "username": data['username'],
                           "password": data['password'],
                           "code": code})
                send_mail_task.delay('کد تایید', code, [data['email']])
            else:
                forms.ValidationError('کد تایید قبلی شما هنوز معتبر است. دو دقیقه دیگر تلاش کنید')

        return data


class VerifyAccountForm(forms.Form):
    code = forms.CharField(
        widget=forms.TextInput(attrs={"class": 'sign__input', "placeholder": 'کد تایید'}),
        error_messages=error_msg
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(VerifyAccountForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = persian_to_english(self.cleaned_data.get('code'))

        if len(code) != 4:
            raise forms.ValidationError('کد تایید وارد شده صحیح نمی باشد')

        session_info = self.request.session.get('register_info', {})
        if not session_info:
            return redirect('accounts:register')
        cache_info = cache.get(session_info.get('username'))
        if not cache_info:
            return redirect('accounts:register')
        cache_code = cache_info.pop('code')
        if code != cache_code:
            raise forms.ValidationError('کد وارد شده صحیح نمی باشد')

        if not session_info == cache_info:
            cache.delete(key=session_info.get('username'))
            del self.request.session['register_info']
            return redirect('accounts:register')

        user = get_user_model().objects.create_user(
            username=cache_info['username'], email=cache_info['email'], password=cache_info['password'])
        del self.request.session['register_info']
        login(request=self.request, user=user, backend='django.contrib.auth.backends.ModelBackend')

        return code


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": 'sign__input', "placeholder": 'ایمیل'}),
        error_messages=error_msg
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ForgetPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        has_user = get_user_model().objects.filter(email=email).exists()
        if not has_user:
            raise forms.ValidationError('ایمیل وارد شده ثبت نشده است')
        if self.request.session.get('forget_info', None):
            if self.request.session['forget_info']['time'] >= 10:
                raise forms.ValidationError('شما بیش از حد مجاز درخواست فرستاده اید')
            else:
                self.request.session['forget_info']['time'] += 1
                self.request.session.modified = True
        else:
            self.request.session['forget_info'] = {"email": email, "time": 1}
        code = otp_code()
        cache.set(key=email, value=code, timeout=120)
        send_mail_task.delay('کد تایید', code, [email])
        return email


class ForgetPasswordVerifyForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(
        attrs={"class": 'sign__input', "placeholder": 'کد تایید'}), error_messages=error_msg
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ForgetPasswordVerifyForm, self).__init__(*args, **kwargs)

    def clean_code(self):
        code = persian_to_english(self.cleaned_data.get('code'))
        if len(code) != 4:
            raise forms.ValidationError('کد وارد شده صحیح نمی باشد')

        forget_info = self.request.session.get('forget_info')
        if not forget_info:
            return redirect('accounts:forget')

        cache_code = cache.get(key=forget_info.get('email'))
        if not cache_code:
            return redirect('accounts:forget')
        if code != cache_code:
            raise forms.ValidationError('کد وارد شده صحیح نمی باشد')

        user = get_user_model().objects.filter(email=forget_info.get('email'))
        if user.exists():
            new_pass = str(randint(10000000, 999999999))
            use = user.first()
            use.set_password(new_pass)
            use.save()
            send_mail_task('رمز عبور جدید شما', new_pass, [forget_info.get('email')])

        return code
