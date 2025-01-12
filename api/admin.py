from django.contrib import admin
from .models import User, Post, Hashtag, Follower, Like, Comment, Notification, Message

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_active', 'is_staff')

class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp')
    search_fields = ('user__username', 'content')
    list_filter = ('timestamp',)

class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('user', 'follower')
    search_fields = ('user__username', 'follower__username')

class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')
    search_fields = ('user__username', 'post__content')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'timestamp')
    search_fields = ('user__username', 'post__content', 'content')
    list_filter = ('timestamp',)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    search_fields = ('user__username', 'message')

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')

# Register models with the admin site
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Follower, FollowerAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(Message, MessageAdmin)