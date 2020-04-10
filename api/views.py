import asyncio

import aioruz
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api import models, serializers, exceptions
from api.serializers import UserSerializer


async def get_student_by_email_async(email):
    try:
        student = await aioruz.student_info(email)
        return student
    except LookupError:
        return None


def get_student_by_email(email):
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(get_student_by_email_async(email))
    return result


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProblemSerializer

    def get_queryset(self):
        try:
            return models.Problem.objects.all().order_by('-id').filter(author=self.request.user.id)
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        return Response(self.serializer_class.data)

    def create(self, request, *args, **kwargs):
        try:
            if request.data['status'] is None:
                request.data['status'] = models.Problem.Status.OPEN

            models.Problem.objects.create(
                author=request.user,
                title=request.data['title'],
                description=request.data['description'],
                status=request.data['status']
            )

            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            pk = int(kwargs['pk'])
            author = request.user

            models.Problem.objects.get(id=pk).delete()

            return Response(status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MessagesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        try:
            # kek = get_student_by_email('vaafnnenkov@edu.hse.ru')
            return models.Message.objects.all().order_by('id')
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        return Response(self.serializer_class.data)

    def create(self, request, *args, **kwargs):
        try:
            problem = None
            if 'problem' in request.data and request.data['problem'] != 0:
                problem = request.data['problem']

            dormitory = None
            if 'dormitory' in request.data and request.data['dormitory'] != 0:
                dormitory = request.data['dormitory']

            models.Message.objects.create(
                author=request.user,
                text=request.data['text'],
                problem_id=problem,
                dormitory_id=dormitory
            )

            return Response(status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response({"Fail": ex}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_auth(request):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        send_mail('Код подтверждения', 'Ваш код подтверждения.', 'confrim@hsesupporter.ru',
                  ['vaannenkov@edu.hse.ru'], fail_silently=False)
        User.objects.create_user(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


class DormitoriesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DormitorySerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        try:
            return models.Dormitory.objects.all()
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        if request.user is not None:
            return Response(self.serializer_class.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class NoticesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NoticeSerializer

    def get_queryset(self):
        try:
            return models.Notice.objects.all().order_by('-id')
        except TypeError:
            raise exceptions.Unauthorized()

    def get(self, request):
        if request.user is not None:
            return Response(self.serializer_class.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
