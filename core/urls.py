
from django.urls import path

from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),

    path('add-blog', views.add_blog, name='add-blog'),
    path('see-blogs', views.see_blogs, name='see-blog'),
    path('logout',views.logout_page,name='logout'),

    path('blog-details/<id>', views.blog_details, name='blog-details'),

    path('delete-blog/<id>', views.delete_blog, name='delete-blog'),
    path('update-blog/<id>', views.update_blog, name='update-blog'),
    path('search/', views.search_view, name='search'),

]

