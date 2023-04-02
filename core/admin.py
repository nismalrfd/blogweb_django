from django.contrib import admin

from core.models import Comment, BlogModel

# Register your models here.
admin.site.register(BlogModel)
admin.site.register(Comment)