"""Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from blog.upload import upload_image
from blog.views import homeview
urlpatterns = [
    url(r'^admin/media/(?P<dir_name>[^/]+)$',upload_image,name='upload_image'),
    url(r'^blog/',include('blog.urls',namespace='blog',app_name='blog')),
    url(r'^$',homeview),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$',serve,{'document_root': settings.MEDIA_ROOT}),
]
