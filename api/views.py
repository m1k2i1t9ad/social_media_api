from rest_framework import viewsets, permissions, generics
from .models import User, Post, Follower, Like, Comment, Notification, Message, Hashtag
from .serializers import UserSerializer, PostSerializer, FollowerSerializer, LikeSerializer, CommentSerializer, NotificationSerializer, MessageSerializer, HashtagSerializer
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import generics
from rest_framework.permissions import AllowAny
# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            post = serializer.save(user=self.request.user)

            # Extract hashtags from the content
            hashtags = set(word.strip('#') for word in post.content.split() if word.startswith('#'))
            for tag in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=tag)
                post.hashtags.add(hashtag)

            # Create notifications for followers
            for follower in post.user.followers.all():
                Notification.objects.create(user=follower.follower, message=f"{post.user.username} posted a new update.")
        except Exception as e:
            # Return a 400 Bad Request if any error occurs during post creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Follower ViewSet
class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Save the follower relationship with the logged-in user
            serializer.save(follower=self.request.user)

            # Create a notification for the user being followed
            Notification.objects.create(user=serializer.validated_data['user'],
                                        message=f"{self.request.user.username} started following you.")
        except Exception as e:
            # Return a 400 Bad Request if any error occurs during follower creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Like ViewSet
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Check if the user has not already liked the post
            if not Like.objects.filter(user=self.request.user, post=serializer.validated_data['post']).exists():
                serializer.save(user=self.request.user)
                # Create a notification for the post owner
                Notification.objects.create(user=serializer.validated_data['post'].user, message=f"{self.request.user.username} liked your post.")
        except Exception as e:
            # Return a 400 Bad Request if any error occurs during like creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Save the comment with the logged-in user as the author
            comment = serializer.save(user=self.request.user)
            # Create a notification for the post owner
            Notification.objects.create(user=comment.post.user, message=f"{self.request.user.username} commented on your post.")
        except Exception as e:
            # Return a 400 Bad Request if any error occurs during comment creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Notification ViewSet
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter notifications to return only those for the logged-in user
        return self.queryset.filter(user=self.request.user)

# Message ViewSet
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            # Save the message with the logged-in user as the sender
            serializer.save(sender=self.request.user)
        except Exception as e:
            # Return a 400 Bad Request if any error occurs during message creation
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Hashtag ViewSet
class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        names = self.request.GET.getlist('names')
        if not names:
            # Return a 400 Bad Request if no hashtags are provided
            return Response({"error": "No hashtags provided."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter hashtags by names provided in the request
        return self.queryset.filter(name__in=names)

# TrendingPosts ViewSet
class TrendingPostsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        try:
            # Get posts with the highest number of likes
            trending_posts = Post.objects.annotate(like_count=Count('like')).order_by('-like_count')[:10]
            serializer = PostSerializer(trending_posts, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Return a 500 Internal Server Error if any unexpected error occurs
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)