from django.contrib.auth.models import User
from rest_framework import serializers

from api import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class ProblemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Problem
        fields = ['author', 'title', 'description', 'status', 'created_at', 'updated_at']
