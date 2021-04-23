"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from register import views as vreg

from django.conf.urls.static import static
from django.conf import settings
from rest_framework.authtoken import views


urlpatterns = [
	path('s/',include('snippets.urls')),
    path('admin/', admin.site.urls),
    path('', include("store.urls")), #eğer domainde bişi yazmıyosa maine yolla
    path("register/", vreg.register, name="register" ),
    path('', include("django.contrib.auth.urls")), 
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token, name='api-token-auth'),
    path("api/", include("api.urls", namespace='api')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)