from rest_framework import serializers
from user.models import *
from rest_framework.utils import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','website_url','role','email']


class CommenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commenter
        fields = ['id','username','website_url','role','email']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id','username','website_url','role','email']
    

class FollowerFollowingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()

    class Meta:
        model = Follower
        fields = ['user','followers','following']

    def get_user(self,obj):
        return f"{obj.user}"
    
    def get_followers(self, obj):
        followers = Follower.objects.filter(user=obj.user)
        follower_names = [follower.follower.username for follower in followers]
        return follower_names
    
    def get_following(self, obj):
        followers = Follower.objects.filter(follower=obj.user)
        follower_names = [follower.user.username for follower in followers]
        return follower_names