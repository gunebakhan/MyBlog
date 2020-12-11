from django.shortcuts import render, redirect
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


    print('request.user.is_authenticated', request.user.is_authenticated)

    if request.user.is_authenticated:
        logged = True
    else:
        logged = False

    context = {
    'categories': categories,
    'posts': posts,
    'post_dates': post_dates, 
    'logged': logged
    }

    return render(request, 'home/index.html', context)



def single(request, slug):
    categories = Category.objects.all()
    try:
        post = Post.objects.select_related('post_setting').get(slug=slug)
        comments = Comment.objects.filter(post=post)
    except Post.DoesNotExist:
        raise Http404('Post not found')

    if request.user.is_authenticated:
        logged = True
    else:
        logged = False
    context = {
        'post': post,
        'categories': categories,
        'settings': post.post_setting,
        'comments': comments,
        'logged': logged
    }
    # print(comments.values())
    return render(request, 'blog/post_single.html', context)


def categories(request, slug):
    posts = Post.objects.filter(category__slug=slug)
    categories = Category.objects.all()

    if request.user.is_authenticated:
        logged = True
    else:
        logged = False
    context = {
        'posts': posts,
        'categories': categories,
        'logged': logged
    }
    
    return render(request, 'blog/archives.html', context)

