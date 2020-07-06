"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"account/",include("account.url",namespace="account")),
    path("",include("blogs.urls",namespace="blog")),
    path("comment/",include("comment.url",namespace="comment")),
    path("collected/",include("collection.urls",namespace="collected")),
    path(r"ckeditor/",include("ckeditor_uploader.urls")),
    path(r"oauth/",include("oauth.urls",namespace="oauth")),
    path(r'froala_editor/', include('froala_editor.urls')),
    path(r"notification/",include("notifications.urls",namespace="notification")),
    path(r"notice/",include("notice.urls",namespace="notice")),
    path(r"appeal",include("appeal.urls",namespace="appeal"))
]
urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
