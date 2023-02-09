from pyexpat import model
from .models import Post,Comment
from django.contrib.auth.models import User
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id','user', 'post', 'time_stamp', 'content', 'slug')

class PostSerializer(serializers.ModelSerializer):
    comments= CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id','title', 'content', 'image', 'category', 'publish_date', 'last_updated', 'author', 'status', 'slug', 'comment_count', 'view_count', 'like_count', 'comments')

class PostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title', 'content', 'image', 'category',  'author', 'status')

class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'post', 'content')

class CommentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('user', 'post', 'content')


class PostUpdateSerializer(serializers.ModelSerializer):
        comments = CommentSerializer(many=True)
    
        class Meta:
            model = Post
            fields = ('id','title', 'content', 'image', 'category', 'publish_date', 'last_updated', 'author', 'status', 'slug', 'comment_count', 'view_count', 'like_count', 'comments')


