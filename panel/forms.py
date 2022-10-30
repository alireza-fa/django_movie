from django import forms
from django.contrib.auth import get_user_model


class UserForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'is_admin', 'role', 'username', 'email')
        widgets = {
            "first_name": forms.TextInput(attrs={"class": 'sign__input', "id": 'first_name'}),
            "last_name": forms.TextInput(attrs={"class": 'sign__input', "id": 'last_name'}),
            "username": forms.TextInput(attrs={"class": 'sign__input', "id": 'username'}),
            "email": forms.EmailInput(attrs={"class": 'sign__input', "id": 'email'}),
            "role": forms.Select(attrs={"class": 'js-example-basic-single', "id": 'rights'}),
        }
