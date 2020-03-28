from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'dormitories', views.DormitoriesViewSet, basename='Dormitories')
router.register(r'problems', views.ProblemViewSet, basename='Problems')
router.register(r'messages', views.MessagesViewSet, basename='Messages')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('djoser.urls.authtoken')),
]
