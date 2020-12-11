from django.urls import path, include
from .views import home, single, categories, login_view, logout_view


urlpatterns = [
    path('', home, name='home'),
    path('posts/', home, name='posts_archive'),
    path('posts/<slug:slug>', single, name='post_single'),
    path('cats/<slug:slug>', categories, name='cat_archives'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout')
]
