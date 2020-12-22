from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, Http404
from .models import Post, Category, Comment
from django.views.generic.list import ListView
from django.views.generic import DetailView


# Create your views here.

class PostArchiveListView(ListView):
    model = Post
    template_name = 'home/index.html'
    queryset = Post.objects.all()
    paginate_by = 5

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["categories"] = Category.objects.all()
        # context["posts"] = Post.objects.all()
        context["posts_dates"] = Post.objects.dates('publish_time', 'month', order='DESC')
        context['logged'] = True if self.request.user.is_authenticated else False
        return context
    

def home(request):
    # categories = Category.objects.all()
    posts = Post.objects.all()
    post_dates = Post.objects.dates('publish_time', 'month', order='DESC')

    context = {
    'posts': posts,
    'post_dates': post_dates
    }

    return render(request, 'home/index.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_single.html'
    # queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["categories"] = Category.objects.all()
        # context["posts"] = Post.objects.all()
        context["posts_dates"] = Post.objects.dates('publish_time', 'month', order='DESC')
        context['comments'] = context['post'].post_comment.all()
        context['settings'] = context['post'].post_setting
        return context


def single(request, category, slug):
    # categories = Category.objects.all()
    try:
        post = Post.objects.select_related('post_setting').get(slug=slug)
        comments = Comment.objects.filter(post=post)
    except Post.DoesNotExist:
        raise Http404('Post not found')

    context = {
        'post': post,
        'settings': post.post_setting,
        'comments': comments
    }

    return render(request, 'blog/post_single.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = "blog/archives.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(category__slug=self.kwargs['slug'])
        # context['categories'] = Category.objects.all()
        # if request.user.is_authenticated:
        #     logged = True
        # else:
        #     logged = False
        # context = {
        #     'posts': posts,
        #     'categories': categories,
        #     'logged': logged
        # }
        
        return context
    


def categories(request):
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return context

# def categories(request, slug):
#     posts = Post.objects.filter(category__slug=slug)
#     categories = Category.objects.all()

#     context = {
#         'posts': posts,
#         'categories': categories
#     }
    
#     return render(request, 'blog/archives.html', context)




