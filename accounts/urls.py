from django.urls import path, include
from .views import login_view, logout_view, AdminLogin, accounts_register, password_reset, activate, profile


urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', AdminLogin.as_view(), name='login'),
    path('register/', accounts_register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password_rest/', password_reset, name='password_reset'),
    path('profile/', profile, name='profile'),
    path('activate/<slug:uidb64>/<slug:token>)/',
         activate, name='activate'),
]
