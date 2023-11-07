from django.forms import ModelForm
from django import forms


from core.models import BlogModel, Comment

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class BlogForm(ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title','content','image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'content': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            }),
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']