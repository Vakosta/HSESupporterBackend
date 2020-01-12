from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

from api import models, serializers, exceptions


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProblemSerializer

    def get_queryset(self):
        try:
            return models.Problem.objects.filter(author=self.request.user)
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        return Response(self.serializer_class.data)

    def create(self, request, *args, **kwargs):
        return models.Problem.objects.create(request.data)
