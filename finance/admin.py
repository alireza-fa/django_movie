from django.contrib import admin

from .models import Plan, PlanAttribute, Gateway, Payment, PlanDiscount, UserPlan


class PlanAttributeInline(admin.TabularInline):
    model = PlanAttribute


class PlanDiscountInline(admin.TabularInline):
    model = PlanDiscount


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = (PlanAttributeInline, PlanDiscountInline)


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    pass
