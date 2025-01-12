from django.contrib.auth.models import AbstractUser,Group,Permission
from django.db import models
from cloudinary.models import CloudinaryField
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)  # Optional Bio
    profile_picture = models.ImageField(upload_to='profile_pictures/',blank=True, null=True)  # Optional Profile Picture
    location = models.CharField(max_length=100, blank=True, null=True)  # User location
    website = models.URLField(blank=True, null=True)  # User website
    cover_photo = models.ImageField(upload_to='cover_photos/',blank=True, null=True)  # Cover photo URL
      # Override the default related_name to avoid clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change this to avoid clashes
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change this to avoid clashes
        blank=True,)

class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.ImageField('media',blank=True, null=True)  # Media URL for images/videos
    hashtags = models.ManyToManyField('Hashtag',related_name="posts",blank=True)  # Many-to-many relationship with hashtags

    
    def __str__(self):
        
        return f"{self.user.username}: {self.content[:20]}..."
    
class Hashtag(models.Model):
    name = models.CharField(max_length=30, unique=True)  # Unique hashtag name

class Follower(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'follower')
        
    def save(self, *args, **kwargs):
        # Prevent a user from following themselves
        if self.user == self.follower:
            raise ValidationError("You cannot follow yourself.")
        super().save(*args, **kwargs)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')  # A user can like a post only once

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User to notify
    message = models.TextField()  # Notification message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notification was created

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()  # Message content
    timestamp = models.DateTimeField(auto_now_add=True)  # Message sent timestamp
