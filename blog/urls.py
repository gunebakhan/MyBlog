from django.urls import path, include
from . import views
from django.views.decorators.http import require_POST, require_GET
from .api import post_list, comment_list, comment_detail, post_detail, PostList, PostDetail


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
    path('api/posts/', PostList.as_view(), name="post_list"),
    path('api/posts/<int:pk>/', PostDetail.as_view(), name="post_detail"),
    path('api/comments/', comment_list, name="comment_list"),
    path('api/comments/<int:pk>/', comment_detail, name="comment_detail"),
]
