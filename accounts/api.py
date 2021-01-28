from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from .models import User
# User = get_user_model()

class UserViewSet(viewsets. ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class PostViewSet(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(draft=False)