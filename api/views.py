import asyncio
import string

import aioruz
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import viewsets, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api import models, serializers, exceptions
from api.exceptions import WrongEmail, CodeConfirmationException


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


class AuthView(views.APIView):
    def post(self, request):
        try:
            email = request.data['email']
            student = get_student_by_email(email)
            if student is None:
                raise WrongEmail

            code = get_random_string(length=6, allowed_chars='1234567890')
            models.Confirmation.objects.create(
                email=email,
                code=code,
            )

            User.objects.create_user(
                email=email,
                username=email,
                password='thisishadrkey'
            )

            send_mail('Код подтверждения',
                      'Ваш код подтверждения: {}'.format(code),
                      'confrim@hsesupporter.ru',
                      [email],
                      fail_silently=False)

            return Response(
                {
                    'message': 'Код подтверждения отправлен на почту.',
                    'student': {
                        'fio': student['fio'],
                        'info': student['info'],
                    },
                },
                status=status.HTTP_200_OK)

        except WrongEmail as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except KeyError as e:
            return Response({'message': 'Вы не передали один из параметров'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


class AuthConfirmView(views.APIView):
    def post(self, request):
        try:
            email = request.data['email']
            code = request.data['code']

            student = get_student_by_email(email)
            if student is None:
                raise WrongEmail

            confirmation = models.Confirmation.objects.get(email=email, code=code)
            if confirmation is None:
                raise CodeConfirmationException
            confirmation.delete()

            user = models.User.objects.get(email=email)
            if user is None:
                raise CodeConfirmationException

            token = get_random_string(length=6, allowed_chars=(string.ascii_letters + string.digits))
            Token.objects.create(
                user=user,
                key=token,
            )

            return Response(
                {
                    'message': 'Успешная авторизация.',
                    'token': token,
                    'student': {
                        'fio': student['fio'],
                        'info': student['info'],
                    },
                }, status=status.HTTP_200_OK)

        except CodeConfirmationException as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except WrongEmail as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except KeyError as e:
            return Response({'message': 'Вы не передали один из параметров'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': e}, status=status.HTTP_400_BAD_REQUEST)


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
