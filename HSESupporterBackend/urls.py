from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()

router.register(r'notices', views.NoticesViewSet, basename='Notices')
router.register(r'problems', views.ProblemViewSet, basename='Problems')
router.register(r'messages', views.MessagesViewSet, basename='Messages')
router.register(r'dormitories', views.DormitoriesViewSet, basename='Dormitories')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),

    path('auth/register/', views.AuthView.as_view()),
    path('auth/register/confirm-email/', views.AuthConfirmView.as_view()),
    path('auth/accept-status/', views.AcceptStatusView.as_view()),

    path('profile/', views.ProfileView.as_view()),

    path('auth/', include('djoser.urls.authtoken')),
]
