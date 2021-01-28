from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


User = get_user_model()


# Create your models here.
class Category(models.Model):

    title = models.CharField(_("Title"), max_length=50)
    slug = models.SlugField(_("Slug"), unique=True, db_index=True)
    parent = models.ForeignKey("self", verbose_name=_("Parent"), on_delete=models.SET_NULL, null=True, blank=True,
        related_name='children', related_query_name='children')

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.slug


class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(draft=False)

    objects = models.Manager()
    newManager = NewManager()
    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True, unique_for_date='publish_time')
    content = models.TextField(_("Content"))
    create_at = models.DateTimeField(_("Create at"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True, auto_now_add=False)
    publish_time = models.DateTimeField(_("Publish at"), db_index=True)
    draft = models.BooleanField(_("Draft"), db_index=True, default=True)
    image = models.ImageField(_("Image"), upload_to="media/post/images")
    category = models.ForeignKey("blog.Category", verbose_name=_("Category"), on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_name='posts', related_query_name='posts')

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("post_single", args=[self.category.slug, self.slug])
        # return reverse("post_single", args=[self.slug])



class PostSetting(models.Model):

    post = models.OneToOneField("blog.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name='post_setting', related_query_name='post_setting')
    comment = models.BooleanField(_("Comment"), default=False)
    author = models.BooleanField(_("Author"), default=False)
    allow_discussion = models.BooleanField(_("Allow Discussion"), default=True)

    class Meta:
        verbose_name = _("PostSetting")
        verbose_name_plural = _("PostSettings")

    def __str__(self):
        return self.post.title


class CommentLike(models.Model):

    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    comment = models.ForeignKey("blog.Comment", verbose_name=_("Comment"), on_delete=models.CASCADE, related_name='comment_like', related_query_name='comment_like')
    condition = models.BooleanField(_("Condition"))
    create_at = models.DateTimeField(_("Create at"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True, auto_now_add=False)

    class Meta:
        unique_together = [['author', 'comment']]
        verbose_name = _("CommentLike")
        verbose_name_plural = _("CommentLikes")

    def __str__(self):
        return str(self.condition)


class Comment(MPTTModel):
    post = models.ForeignKey(Post, verbose_name=_("Post"), on_delete=models.CASCADE, related_name="comments")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_query_name='children')
    # author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE, related_query_name='comments')
    name = models.CharField(_("Name"), max_length=50)
    email = models.EmailField(_("Email"), max_length=254)
    content = models.TextField(_("Content"))
    publish = models.DateTimeField(_("Publish"), auto_now=False, auto_now_add=True)
    status = models.BooleanField(_("Status"), default=True)

    class MPTTMeta:
        order_insertion_by = ['publish']
    
    def __str__(self):
        return f"Comment by {self.name}"



def like_comment(request):
    
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
