from django.urls import path
from .views import home, single, categories


urlpatterns = [
    path('', home, name='home'),
    path('posts/', home, name='posts_archive'),
    path('posts/<slug:slug>', single, name='post_single'),
    path('cats/<slug:slug>', categories, name='cat_archives')
]
