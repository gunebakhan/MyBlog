from django import forms
from .models import Comment, Category
from mptt.forms import TreeNodeChoiceField

class CommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False
        self.fields['parent'].label = ''
        self.fields['parent'].widget.attrs.update({'class': 'd-none'})
    class Meta:
        model = Comment
        fields = ("name", "parent", "email", "content")
        labels = {
            'name': '',
            'email': '',
            'content': ''
        }
        widgets = {
            "name": forms.TextInput(attrs={'class': 'col-sm-12', 'placeholder': 'نام', 'label': 's'}),
            "email": forms.TextInput(attrs={'class': 'col-sm-12', 'placeholder': 'ایمیل'}),
            "content": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'نظرتان را اینجا بنویسید', 'style':'resize:none;'})
        }

class PostSearchForm(forms.Form):
    q = forms.CharField()
    c = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by('title'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['c'].label = ''
        self.fields['c'].required = False
        self.fields['c'].label = 'دسته بندی'
        self.fields['q'].label = 'جستجو برای'
        self.fields['q'].widget.attrs.update(
            {'class': 'form-control menudd'})
        self.fields['q'].widget.attrs.update(
            {'data-toggle': 'dropdown'})