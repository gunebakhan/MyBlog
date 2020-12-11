from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate

class DivErrorList(forms.ValidationError):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return ''
        return '<div class="errorlist">%s s s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self])

class LoginForm(forms.Form):
    username = forms.CharField(label=_('نام کاربری'), max_length=80)
    password = forms.CharField(label=_('رمز عبور'), max_length=80, widget=forms.PasswordInput)
    error_class = DivErrorList

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control form-text','placeholder':'نام کاربری را وارد کنید'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'رمز عبور را وارد کنید', 'id': 'exampleInputPassword1'})
    

    def clean_username(self):
        username = self.cleaned_data["username"]
        
        if len(username) < 4:
            raise forms.ValidationError("طول نام کاربری باید بزگتر از 3 کاراکتر باشد.", code='invalid')


        return username
    
    def clean_password(self):
        data = self.cleaned_data["password"]
        
        if len(data) < 7:
            raise forms.ValidationError("طول رمز عبور باید بزگتر از 7 کاراکتر باشد.", code='invalid')
        return data
    


    
    
