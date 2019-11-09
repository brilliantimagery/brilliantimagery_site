import uuid

from django import forms
from tinymce import TinyMCE

from post.models import PostComment


class NewCommentForm(forms.ModelForm):
    # comment = forms.CharField(widget=TinyMCE(mce_attrs={}))
    comment = forms.CharField(widget=TinyMCE(attrs={'placeholder': 'hello', 'id': 'lkj'}), max_length=10000)

    class Meta:
        model = PostComment
        fields = ['username', 'email', 'comment']
        widgets = {
            'username': forms.TextInput(attrs={'class': '',
                                               'placeholder': 'Nickname',
                                               }),
            'email': forms.EmailInput(attrs={'class': '',
                                             'placeholder': 'Email Address',
                                             }),
            # 'comment': forms.TextInput(attrs={'class': '',
            #                                   'placeholder': 'Comment',
            #                                   }),
        }
        