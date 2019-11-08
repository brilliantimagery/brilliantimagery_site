from django import forms

from post.models import PostComment


class NewCommentForm(forms.ModelForm):
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
            'comment': forms.TextInput(attrs={'class': '',
                                              'placeholder': 'Comment',
                                              }),
        }
        