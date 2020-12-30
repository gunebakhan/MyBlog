from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseForbidden
from .models import Post, Category, Comment
from django.views.generic.list import ListView
from django.views.generic import DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from .forms import CommentForm, PostSearchForm
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Q
import json
from .models import CommentLike


# Create your views here.

class PostArchiveListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    queryset = Post.objects.all()
    paginate_by = 3
    queryset = Post.newManager.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["categories"] = Category.objects.all()
        # context["posts"] = Post.objects.all()
        context["posts_dates"] = Post.objects.dates('publish_time', 'month', order='DESC')
        # context['logged'] = True if self.request.user.is_authenticated else False
        return context
    
######################## CBV ################################
# class PostDisplay(DetailView):
#     model = Post
#     template_name = 'blog/post_single.html'
#     queryset = Post.newManager.all()


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["posts_dates"] = Post.objects.dates('publish_time', 'month', order='DESC')
#         context['comments'] = context['post'].comments.all()
#         context['settings'] = context['post'].post_setting
#         context['comment_form'] = CommentForm()
#         return context

# class CommentView(SingleObjectMixin, FormView):
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'
#     template_name = 'blog/post_single.html'
#     form_class = CommentForm
#     model = Comment

#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         return super().post(request, *args, **kwargs)
    
#     def get_success_url(self):
#         return reverse('post_single', kwargs={'pk': self.object.pk})


# class PostDetail(View):
#     def get(self, request, *args, **kwargs):
#         view = PostDisplay.as_view()
#         return view(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         view = CommentView.as_view()
#         return view(request, *args, **kwargs)
######################## CBV ################################


def post_single(request, category, slug):
    post = get_object_or_404(Post, slug=slug, draft=False)
    post_setting = post.post_setting
    allcomments = post.comments.filter(status=True)
    page = request.GET.get('page', 1)
    paginator = Paginator(allcomments, 6)
    # likes = CommentLike.objects.filter(condition=True).count()
    # dislikes = CommentLike.objects.filter(condition=False).count()
    likes = {}
    dislikes = {}
    author_likes = {}
    author_dislikes = {}
    
    # print(request.user)
    for comment in allcomments:
        likes[comment.id] = CommentLike.objects.filter(comment=comment, condition=True).count()
        dislikes[comment.id] = CommentLike.objects.filter(comment=comment, condition=False).count()

    if request.user.is_authenticated:
        for comment in allcomments:
            author_likes[comment.id] = CommentLike.objects.filter(comment=comment, condition=True, author=request.user)
            author_dislikes[comment.id] = CommentLike.objects.filter(comment=comment, condition=False, author=request.user)

    # print(author_likes)

    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    
    user_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.save()
            return HttpResponseRedirect('/blog/' + category + '/' + slug)
    else:
        comment_form = CommentForm()
    context = {
        'post': post,
        'user_comments': user_comment,
        'comments': user_comment,
        'comment_form': comment_form,
        'page_comments': comments,
        'settings': post.post_setting,
        'allcomments': allcomments,
        'likes': likes,
        'dislikes': dislikes,
        'author_likes': author_likes,
        'author_dislikes': author_dislikes
    }

    # print(context)

    return render(request, 'blog/post_single.html', context)


# def single(request, category, slug):
#     # categories = Category.objects.all()
#     try:
#         post = Post.objects.select_related('post_setting').get(slug=slug)
#         comments = Comment.objects.filter(post=post)
#     except Post.DoesNotExist:
#         raise Http404('Post not found')

#     context = {
#         'post': post,
#         'settings': post.post_setting,
#         'comments': comments
#     }

#     return render(request, 'blog/post_single.html', context)


class CategoryListView(ListView):
    model = Category
    template_name = "blog/archives.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(category__slug=self.kwargs['slug'])
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


def search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.objects.filter(title__contains=search_string)[:5]
            data = serializers.serialize('json', list(search_string), fields=('id', 'title', 'slug', 'category'))
            return JsonResponse({'search_string': data})

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'blog/search.html',
                  {'form': form,
                   'q': q,
                   'results': results})


def like_comment(request):
    user = request.user
    if request.POST.get('action') == 'post':
        comment_id = str(request.POST.get('id'))
        comment_id = json.loads(comment_id)
        like_type = str(request.POST.get('like_type'))
        if like_type == 'like':
            status = True
        else:
            status = False
        comment = Comment.objects.get(id=comment_id)
        comment_like = CommentLike(author=user, comment=comment, condition=status)
        comment_like.save()
        like_counts = CommentLike.objects.filter(comment=comment, condition=status).count()
        response = {'like_counts': like_counts}
        response = json.dumps(response)
        return HttpResponse(response, status=201)
    
    return HttpResponse(json.dumps({'comment_id': -1}))


def add_comment(request):
    if request.POST.get('action') == 'post':
        post_id = int(request.POST.get('post_id'))
        comment = Comment(name=request.POST.get('author'), 
                        email=request.POST.get('email'),
                        content=request.POST.get('content'),
                        post_id=post_id)
        comment.save()
        print(comment.publish)
        counts = Comment.objects.all().count()

        return HttpResponse(json.dumps({'counts': counts}), status=201)