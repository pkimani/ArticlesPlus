"""
URL configuration for djrssproj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from rssapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rssapp.urls')),  # Include the URLs from the 'rssapp' app
    path('api/start_rss_feed_download/', views.start_rss_feed_download, name='start_rss_feed_download'),
    path('api/start_openai_query/', views.start_openai_query, name='start_openai_query'),
    # No need for other URL patterns here since the frontend will be served by Nginx
]