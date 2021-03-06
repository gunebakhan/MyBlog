from django.urls import path, include
from . import views
from django.views.decorators.http import require_POST, require_GET
from .api import *
from rest_framework.urlpatterns import format_suffix_patterns
from MyBlog.urls import router




router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)


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
    # path('cats/<slug:slug>', views.categories, name='cat_archives'),
    # path('api/', include(router.urls)),
    path('<slug:slug>/', views.CategoryListView.as_view(), name='cat_archives'),
    # path('api/posts/', PostViewSet.as_view({'get': 'list', 'post': 'create'}), name="post_list"),
    # path('api/posts/<int:pk>/', PostViewSet.as_view({'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name="post_detail"),
    # path('api/comments/', comment_list, name="comment_list"),
    # path('api/comments/<int:pk>/', comment_detail, name="comment_detail"),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
