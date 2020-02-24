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


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Message
        fields = ['author', 'text', 'is_read', 'created_at', 'updated_at']


class DormitorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Dormitory
        fields = ['name', 'address', 'students']
