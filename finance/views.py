from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import PayPlanForm
from .models import Payment


class PlanPayView(LoginRequiredMixin, View):
    form_class = PayPlanForm

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.is_valid(form)
        else:
            return redirect('/')

    def is_valid(self, form):
        cd = form.cleaned_data
        payment = Payment.create(self.request.user, cd['value'], cd['gateway'])
        if payment:
            link_request = payment.get_link_request()
            if link_request:
                return redirect(link_request)
            return redirect('finance/field_pay.html')
        return redirect('/')


class PlanPayVerify(LoginRequiredMixin, View):
    template_name = 'finance/verify.html'

    def get(self, request):
        payment = get_object_or_404(Payment.objects.all(), authority=request.GET.get('Authority'))
        status, data = payment.verify(request=request)
        if status and data:
            if status == 100:
                return render(request, self.template_name, {"message": f'success, ref_if: {data["ref_id"]}'})
            elif status == 101:
                return render(request, self.template_name, {"message": data['message']})
            else:
                return render(request, self.template_name, {"message": data['message']})
        return render(request, self.template_name, {"message": 'error, please try again.'})
