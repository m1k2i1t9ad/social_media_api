"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# from .views import HomeView, follow_users, personalized_feed, create_post,dashboard

admin.site.site_header="Socialmedia Admin"
admin.site.index_title="Admin"

urlpatterns = [

    # path('', , name='home'),  # Home page URL
    path('api/', include('api.urls')),  # Including the API URLs
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
