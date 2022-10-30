from django import forms

from .models import MovieComment, MovieReview


error_msg = {
    "invalid": 'مقدار وارد شده معتبر نمی باشد',
    "required": 'این فیلد نمی تواند خالی باشد'
}


class CommentMovieForm(forms.ModelForm):
    class Meta:
        model = MovieComment
        fields = ('body',)
        widgets = {
            "body": forms.Textarea(attrs={"class": 'sign__textarea', "placeholder": 'چیزی بنویسید...'})
        }
        error_messages = {"body": error_msg}


class ReviewMovieForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ('subject', 'rate', 'description')

        error_messages = {
            "subject": error_msg,
            "rate": error_msg,
            "description": error_msg
        }
