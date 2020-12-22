from django.urls import path, include
from .views import home, single, categories, PostArchiveListView, PostDetailView, CategoryListView


urlpatterns = [
    # path('', home, name='home'),
    path('', PostArchiveListView.as_view(), name='home'),
    # path('posts/', home, name='posts_archive'),
    # path('posts/<slug:category>/<slug:slug>', single, name='post_single'),
    path('posts/<slug:category>/<slug:slug>', PostDetailView.as_view(), name='post_single'),
    # path('cats/<slug:slug>', categories, name='cat_archives')
    path('cats/<slug:slug>', CategoryListView.as_view(), name='cat_archives')
]
