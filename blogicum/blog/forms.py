from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'pub_date': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={'type': 'datetime-local'}
            )
        }
        exclude = ('author',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
