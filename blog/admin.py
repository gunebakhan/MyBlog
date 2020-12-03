from django.contrib import admin
from django.contrib import messages
from .models import Post, PostSetting, Comment, CommentLike, Category
from django.utils.translation import ungettext

# Register your models here.
class PostItemInline(admin.StackedInline):
    model = PostSetting
    fields = ('author', 'comment', 'allow_discussion')
    extra = 1
    show_change_link = True



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'create_at', 'update_at', 'publish_time', 'draft', 'category', 'author')
    date_hierarchy = 'publish_time'
    lisdt_filter = ('author',)
    inlines = [PostItemInline]
    # value of empty fields
    empty_value_display = '-empty-'
    prepopulated_fields = {"slug": ("title",)}

    # fields that can be shown in admin form
    # fields = ('title', 'slug', 'publish_time', 'image', 'content', 'draft', 'category', 'author')
    # fileds that are excluded from admin form
    # exclude = ('create_at', 'update_at')
    #dictionary of information about the fieldset, including a list of fields to be displayed in it.
    # we cannot use fields and field sets together
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'publish_time', 'image', 'content')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('draft', 'category', 'author')
        })
    )
    
    def make_published(self, request, queryset):
        updated = queryset.update(draft=False)
        self.message_user(request, ungettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)


    def make_drafted(self, request, queryset):
        updated = queryset.update(draft=True)
        self.message_user(request, ungettext(
            '%d story was successfully marked as drafted.',
            '%d stories were successfully marked as drafted.',
            updated,
        ) % updated, messages.SUCCESS)
    
    make_drafted.short_description = "Mark selected stories as drafted"
    make_published.short_description = "Mark selected stories as published"
    actions = [make_published, make_drafted]


class CategoryChildrenItemInline(admin.TabularInline):
    model = Category
    fields = ('title', 'slug')
    extra = 1
    show_change_link = True


class PostChildrenItemInline(admin.TabularInline):
    model = Post
    fields = ('title', 'slug')
    extra = 1
    show_change_link = True



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'parent')
    search_fields = ('slug', 'title')
    list_filter = ('parent',)
    inlines = [CategoryChildrenItemInline, PostChildrenItemInline]



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'is_confirmed', 'author',
                    'like_count', 'dislike_count')
    search_fields = ('content',)
    list_filter = ('is_confirmed',)
    date_hierarchy = 'create_at'
 
admin.site.register(CommentLike)