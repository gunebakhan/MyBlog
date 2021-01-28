from rest_framework import serializers
from .models import Post, Comment, Category
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=250)
#     slug = serializers.SlugField()
#     content = serializers.CharField(style={'base_template': 'textarea.html'})
#     create_at = serializers.DateTimeField(read_only=True)
#     update_at = serializers.DateTimeField(read_only=True)
#     publish_time = serializers.DateTimeField()
#     draft = serializers.BooleanField()
#     image = serializers.ImageField()
    # author_detail = UserSerializer(source='author', read_only=True)
    # author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    
    # def create(self, validated_data):
    #     return Post.newManager.create(**validated_data)

    
    # def update(self, instance, validated_data):
    #     instance.title = validated_data.get('title', instance.title)
    #     instance.slug = validated_data.get('slug', instance.title)
    #     instance.content = validated_data.get('content', instance.content)
    #     instance.publish_time = validated_data.get('publish_time', instance.publish_time)
    #     instance.draft = validated_data.get('draft', instance.draft)
    #     instance.image = validated_data.get('image', instance.image)
    #     instance.save()

    #     return instance


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('id', 'name', 'email', 'content', 'publish')


# class CommentSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=250)
#     email = serializers.EmailField()
#     content = serializers.CharField(style={'base_template': 'textarea.html'})
#     publish = serializers.DateTimeField(read_only=True)

#     def create(self, validate_data):
#         return CommentSerializer2.create(**validate_data)
    

#     def update(self, instance, validate_data):
#         instance.name = validate_data.get('name', instance.name)
#         instance.email = validate_data.get('email', instance.email)
#         instance.content = validate_data.get('content', instance.content)

