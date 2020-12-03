from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Post, Category, Comment


# Create your views here.
def home(request):
    categories = Category.objects.all()
    # iphone = Post.objects.filter(category__slug='iphone').first()
    # microsoft = Post.objects.filter(category__slug='windows10').first()
    posts = Post.objects.all()
    post_dates = Post.objects.dates('publish_time', 'month', order='DESC')
    context = {
        'categories': categories,
        'posts': posts,
        'post_dates': post_dates
    }
    return render(request, 'home/index.html', context)
# def home(request):
#     posts = Post.objects.select_related.all()
#     template = loader.get_template('blog/posts.html')
#     context = {
#         "posts": posts
#     }
#     # return render(request, 'blog/posts.html')
#     return HttpResponse(template.render(context, request))


def single(request, slug):
    categories = Category.objects.all()
    try:
        post = Post.objects.select_related('post_setting').get(slug=slug)
        comments = Comment.objects.filter(post=post)
    except Post.DoesNotExist:
        raise Http404('Post not found')
    context = {
        'post': post,
        'categories': categories,
        'settings': post.post_setting,
        'comments': comments
    }
    # print(comments.values())
    return render(request, 'blog/post_single.html', context)


def categories(request, slug):
    posts = Post.objects.filter(category__slug=slug)
    categories = Category.objects.all()

    context = {
        'posts': posts,
        'categories': categories
    }
    
    return render(request, 'blog/archives.html', context)