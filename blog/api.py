from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins, generics
from rest_framework import viewsets


# class PostViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Post.objects.all()
#         serializer = PostSerializer(queryset, many=True)
#         return Response(serializer.data)
    
#     def


class PostList1(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetail1(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostListMixins(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostDetailMixin(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostList(APIView):
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# @csrf_exempt
# def post_list(request):
#     if request.method == 'GET':
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = PostSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET', 'POST'])
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serizalizer = PostSerializer(post)
        return Response(serizalizer.data)
    
    elif request.method == 'PUT':
        serizalizer = PostSerializer(post, data=request.data)
        if serizalizer.is_valid():
            serizalizer.save()
            return Response(serizalizer.data)
        return Response(serizalizer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
def comment_list(request):
    if request.method == 'GET':
        comments = Comment.objects.filter(status=True)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def comment_detail(request, pk):
    try:
        comment = Comment.objects.get(id=pk)
    except Comment.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)