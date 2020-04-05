from django.contrib.auth.backends import UserModel
from django.contrib.auth.models import User
from rest_framework import serializers

from api import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = [
            'id',
            'url',
            'username',
            'password',
            'email',
            'groups'
        ]


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = [
            'id',
            'author',
            'text',
            'is_read',
            'is_from_student',
            'created_at',
            'updated_at'
        ]


class ProblemSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = models.Problem
        fields = [
            'id',
            'author',
            'title',
            'description',
            'status',
            'created_at',
            'updated_at',
            'messages',
        ]

    def get_messages(self, obj):
        ordered_queryset = models.Message.objects.filter(problem_id=obj.id).order_by('id')
        return MessageSerializer(ordered_queryset, many=True, context=self.context).data


class DormitorySerializer(serializers.HyperlinkedModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = models.Dormitory
        fields = [
            'id',
            'name',
            'address',
            'messages'
        ]

    def get_messages(self, obj):
        ordered_queryset = models.Message.objects.filter(dormitory_id=obj.id).order_by('id')[:20]
        return MessageSerializer(ordered_queryset, many=True, context=self.context).data


class NoticeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Notice
        fields = [
            'id',
            'main_text',
            'text',
            'is_important',
            'created_at',
            'updated_at'
        ]
