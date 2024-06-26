from rest_framework import serializers
from posts.models import *
from django.core.exceptions import ValidationError
from django.db import transaction


class CommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField()
    
    created_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset = Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'

    def get_sub_comments(self, obj):
        sub_comments = obj.sub_comment.all() 
        return CommentSerializer(sub_comments, many=True).data
    
    def get_created_by(self,obj):
        return obj.created_by.username
        
class ReplyOnCommentSerializer(serializers.ModelSerializer):
    reply = serializers.PrimaryKeyRelatedField(queryset = Comment.objects.all(),write_only=True)

    class Meta:
        model = Comment
        fields = ['created_by','post','reply','body']

    def create(self, validated_data):
        main_comment = validated_data.pop('reply',None)
        comment = Comment.objects.create(**validated_data)
        comment.sub_comments = main_comment
        comment.save()
        return comment
            

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True,read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())

    class Meta:
        model = Post
        fields = ['id','body','comments','title','image','created_by']
    
    # for removing the duplicate commetns that are appear in the sub-comments ans actual comments of a same post 
    def to_representation(self, instance):
        represent = super().to_representation(instance)
        seen = set()
        
        def formate_comments(comments):
            unique_comments = []
            for comment in comments:
                if comment['id'] not in seen:
                    seen.add(comment['id'])
                    comment['sub_comments'] = formate_comments(comment['sub_comments'])
                    unique_comments.append(comment)
            return unique_comments
        
        if 'comments' in represent:
            represent['comments'] = formate_comments(represent['comments'])
        return represent


class ThreadSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)
    base_url = serializers.SerializerMethodField(read_only=True)
    complete_url = serializers.SerializerMethodField(read_only=True)
    body = serializers.CharField(write_only=True)
    title = serializers.CharField(write_only=True)
    image = serializers.ImageField(write_only=True)
    created_by = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(),write_only=True)

    class Meta:
        model = Thread
        fields = ['sub_url','post','base_url','complete_url','body','title','image','created_by']
    
    def create(self, validated_data):
        post = {
            'created_by' : validated_data.pop('created_by',None),
            'body' : validated_data.pop('body',None),
            'title' : validated_data.pop('title',None),
            'image' : validated_data.pop('image',None)
        }
        try:
            with transaction.atomic():
                new_post = Post.objects.create(**post)
                thread = Thread.objects.create(post_id=new_post.pk, **validated_data)
                return thread
        except ValidationError as e:
            raise ValidationError(e.message)

    
    def get_base_url(self,obj):
        return obj.base_url
    
    def get_complete_url(self,obj):
        return obj.complete_url


#this serialzers will update the emoji for any posts

class PostLikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['like']

class PostOkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['ok']

class PostLovedUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['loved']

class PostDislikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['dislike']

class PostAngryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['angry']


class CommentLikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['like']

class CommentDislikeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['dislike']

class CommentUpvoteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['upvote']
