from django import forms

from post.models import PostComment


class PostCommentForm(forms.ModelForm):

    class Meta:
        model = PostComment
        