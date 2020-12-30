from django.urls import path, include
from . import views
from django.views.decorators.http import require_POST, require_GET



urlpatterns = [
    # path('', home, name='home'),
    path('', views.PostArchiveListView.as_view(), name='home'),
    # path('posts/', home, name='posts_archive'),
    path('search/', views.search, name='search'),
    path('like/', views.like_comment, name='like_comment'),
    path('add-comment/', views.add_comment, name='add_comment'),
    path('<slug:category>/<slug:slug>', views.post_single, name='post_single'),
    # path('<slug:category>/<slug:slug>', PostDetail.as_view(), name='post_single'),
    # path('posts/<slug:category>/<slug:slug>', require_POST(CommentView.as_view()), name='form_view_url'),
    # path('cats/<slug:slug>', categories, name='cat_archives')
    path('<slug:slug>/', views.CategoryListView.as_view(), name='cat_archives'),
]
