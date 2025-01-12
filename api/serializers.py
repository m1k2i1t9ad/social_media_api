

from rest_framework import serializers
from .models import User, Post, Follower, Like, Comment, Notification, Message, Hashtag

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'email', 'bio', 'profile_picture', 'location', 'website', 'cover_photo']
        extra_kwargs = {'password': {'write_only': True}}  # Exclude password from response 

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    hashtags = serializers.PrimaryKeyRelatedField(queryset=Hashtag.objects.all(), many=True, required=False)
    class Meta:
        model = Post
        fields = ['id', 'content', 'user','timestamp','media', 'hashtags']

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags', [])
        post = Post.objects.create(**validated_data)  # Create the post

        # Add hashtags to the post if they exist
        if hashtags_data:
            post.hashtags.set(hashtags_data)  # Use set() to assign many-to-many relationships

        return post
class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = ['user', 'follower']
        
    def validate(self, attrs):
        if attrs['user'] == attrs['follower']:
            raise serializers.ValidationError("You cannot follow yourself.")
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'content', 'timestamp']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message', 'created_at']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'content', 'timestamp']

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['name']
        
class TrendingPostsSeializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields = ['id', 'content', 'timestamp', 'user']
