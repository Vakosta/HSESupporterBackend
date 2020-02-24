from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response

from api import models, serializers, exceptions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProblemSerializer

    def get_queryset(self):
        try:
            return models.Problem.objects.all()
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        return Response(self.serializer_class.data)

    def create(self, request, *args, **kwargs):
        try:
            models.Problem.objects.create(
                author=request.user,
                title=request.data['title'],
                description=request.data['description'],
                status=request.data['status']
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        try:
            return models.Message.objects.all()
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        return Response(self.serializer_class.data)

    def create(self, request, *args, **kwargs):
        try:
            models.Message.objects.create(
                author=request.user,
                text=request.data['text']
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DormitoriesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DormitorySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            try:
                return models.Dormitory.objects.all()
            except TypeError:
                raise exceptions.Unauthorized()
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        if request.user is not None:
            return Response(self.serializer_class.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
