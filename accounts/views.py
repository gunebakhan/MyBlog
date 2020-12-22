from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.
class AdminLogin(SuccessMessageMixin, LoginView):
    template_name = 'registration/login.html'
    success_message = 'Welcome to your profile'
    



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