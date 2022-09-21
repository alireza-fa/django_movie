from django import forms
from .models import Contact, Magazine


error_msg = {
    "invalid": 'مقدار وارد شده معتبر نمی باشد',
    "required": 'این فیلد نمی تواند خالی باشد'
}


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={"class": 'sign__input', "placeholder": 'نام'}),
            "email": forms.EmailInput(attrs={"class": 'sign__input', "placeholder": 'ایمیل'}),
            "subject": forms.TextInput(attrs={"class": 'sign__input', "placeholder": 'موضوع'}),
            "body": forms.Textarea(attrs={"class": 'sign__input', "placeholder": 'پیام خود را بنویسید . . .'}),
        }
        error_messages = {
            "name": error_msg,
            "email": error_msg,
            "subject": error_msg,
            "body": error_msg,
        }


class MagazineForm(forms.ModelForm):
    class Meta:
        model = Magazine
        fields = ('email',)

    widgets = {
        "email": forms.EmailInput(attrs={"class": 'sign__input', "placeholder": 'ایمیل'})
    }
