from django.urls import path, include
#from rest_framework.urlpatterns import format_suffix_patterns
#from snippets import views
from rest_framework.routers import DefaultRouter
from snippets import views
#from snippets.views import SnippetViewSet, UserViewSet, api_root
#from rest_framework import renderers

#reverse func returns URLS indicated by strings inside
router= DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
path('', include(router.urls)),
]
