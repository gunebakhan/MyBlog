from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.conf import settings
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()



# Create your views here.
class AdminLogin(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = 'Welcome to your profile'
    form_class = LoginForm



def login_view(request):
    alert = False
    if request.user.is_authenticated:
        return redirect('home')
    logged = False
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                logged = True
                login(request, user)
                return redirect('home')
            else:
                alert = True
            
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form, 'logged': logged, 'alert': alert})


def logout_view(request):
    logout(request)
    return redirect('home')

def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('ثبت نام با موفقیت انجام پذیرفت. لینک فعالسازی به ایمیلتان ارسال گردید.')
    else:
        registerForm = RegistrationForm()
    return render(request, 'registration/register.html', {'form': registerForm})


def password_reset(request):
    pass


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'registration/activation_invalid.html')


@login_required
def profile(request):
    return render(request,
                  'accounts/profile.html')