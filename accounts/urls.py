from django.urls import path, include
from .views import login_view, logout_view, AdminLogin


urlpatterns = [
    # path('login/', login_view, name='login'),
    path('login/', AdminLogin.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]
