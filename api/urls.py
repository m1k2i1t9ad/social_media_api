from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import  UserViewSet,UserCreateView, PostViewSet, FollowerViewSet, LikeViewSet, CommentViewSet, NotificationViewSet, MessageViewSet, HashtagViewSet,TrendingPostsViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'followers', FollowerViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'hashtags', HashtagViewSet)
router.register(r'trending', TrendingPostsViewSet, basename='trending_posts')
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('', include(router.urls)),
]