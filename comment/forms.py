from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={
                'class': 'form-control post',
                'style': 'width: 60%;',
            }
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.TextInput(
            attrs={
                'class': 'form-control post',
                'rows': 6,
                'cols': 60,
                'style': 'width: 60%;',
            }
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 5:
            raise forms.ValidationError('内容太短了！')
        return content

    class Meta:
        model = Comment
        fields = {'nickname', 'content'}
