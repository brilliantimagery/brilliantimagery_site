import uuid

from django import forms
from tinymce import TinyMCE

from post.models import PostComment


class NewCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=TinyMCE(attrs={'placeholder': 'hello'}), max_length=10000)

    class Meta:
        model = PostComment
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'class': '',
                                           'placeholder': 'Nickname',
                                           }),
            'email': forms.EmailInput(attrs={'class': '',
                                             'placeholder': 'Email Address',
                                             }),
        }
