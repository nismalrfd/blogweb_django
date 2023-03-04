from django.forms import ModelForm

from core.models import BlogModel, Comment


class BlogForm(ModelForm):
    class Meta:
        model = BlogModel
        fields = ['title','content','image']
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']