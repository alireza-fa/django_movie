from django import template
from django.contrib.auth import get_user_model

from movie.models import Movie, MovieReview, MovieComment, MovieView
from datetime import datetime, timedelta


register = template.Library()


# Actions
def get_last_review():
    return MovieReview.default_manager.all()[:5]


def get_review_count():
    return MovieReview.default_manager.count()


def get_comment_count():
    return MovieComment.default_manager.count()


def get_item_count_per_last_month():
    return Movie.default_manager.filter(created__gte=datetime.now() - timedelta(days=31)).count()


def get_view_count_per_last_month():
    return MovieView.objects.filter(created__gte=datetime.now() - timedelta(days=31)).count()


def get_best_items():
    return Movie.get_best_rates()[:5]


def get_last_items():
    return Movie.default_manager.all().order_by('-created')[:5]


def get_last_users():
    return get_user_model().default_manager.all().order_by('-created')[:5]


@register.filter(name='action_panel')
def action_panel(action):
    actions = {
        "last_reviews": get_last_review,
        "review_count": get_review_count,
        "comment_count": get_comment_count,
        "item_count": get_item_count_per_last_month,
        "view_count": get_view_count_per_last_month,
        "best_items": get_best_items,
        "last_items": get_last_items,
        "last_users": get_last_users,
    }
    func = actions.get(action)
    if func:
        return func()
