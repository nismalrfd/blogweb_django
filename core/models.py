from django.contrib.auth.models import User
from django.db import models
# from froala_editor.fields import FroalaField
from ckeditor.fields import RichTextField


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    token = models.CharField(max_length=100)


class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(upload_to='blog')
    created_at = models.DateTimeField(auto_now_add=True)
    upload_to = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User,related_name='post')

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(BlogModel, related_name='comments', on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)


