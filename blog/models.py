from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


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

    title = models.CharField(_("Title"), max_length=128)
    slug = models.SlugField(_("Slug"), db_index=True, unique=True)
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


class Comment(models.Model):

    content = models.TextField(_("Content"))
    post = models.ForeignKey("blog.Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="post_comment", related_query_name="post_comment")
    author = models.ForeignKey(User, verbose_name=_("Author"), on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(_("Confirm"))
    create_at = models.DateTimeField(_("Create at"), auto_now=False, auto_now_add=True)
    update_at = models.DateTimeField(_("Update at"), auto_now=True, auto_now_add=False)


    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-create_at']


    def __str__(self):
        return self.post.title
    

    @property
    def like_count(self):
        counts = CommentLike.objects.filter(comment=self, condition=True).count()
        return  counts
    

    @property
    def dislike_count(self):
        # counts = CommentLike.objects.filter(comment=self, condition=False).count()
        counts = self.comment_like.filter(condition=False).count()
        return counts




