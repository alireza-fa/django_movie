from django import forms

from .models import Payment, Plan


class PayPlanForm(forms.Form):
    value = forms.IntegerField()
    gateway = forms.IntegerField()
