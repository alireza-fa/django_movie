from django import template

from ..models import Plan, Gateway


register = template.Library()


def get_plans():
    return Plan.objects.all()


def get_gateways():
    return Gateway.objects.filter(is_active=True)


@register.filter(name='finance_actions')
def action(value):
    actions = {
        "plans": get_plans,
        "gateways": get_gateways,
    }

    act = actions.get(value, None)
    if act:
        return act()
