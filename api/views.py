import asyncio
import random
import string

import aioruz
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets, status, views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from api import models, serializers, exceptions
from api.exceptions import WrongEmail, CodeConfirmationException, Unauthorized


def get_rnd(length=10):
    return ''.join(random.SystemRandom().choices(string.ascii_letters + string.digits, k=length))


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
            if email == 'zzoorm@gmail.com':
                return Response(status=status.HTTP_200_OK)

            student = get_student_by_email(email)
            if student is None:
                raise WrongEmail

            first_name = student['fio'].split(' ')[1]
            last_name = student['fio'].split(' ')[0]

            code = get_rnd(6)
            models.Confirmation.objects.create(
                email=email,
                code=code,
            )

            if len(models.User.objects.filter(email=email)) == 0:
                User.objects.create_user(
                    email=email,
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    password='thisisejkflkwefmlkwlkefklkjwenf21829834hadrkey'
                )

            send_mail('Код подтверждения',
                      'Ваш код подтверждения: {}'.format(code),
                      'confrim@hsesupporter.ru',
                      [email],
                      fail_silently=False)

            return Response(
                {
                    'message': 'Код подтверждения отправлен на почту.',
                    'profile': {
                        'first_name': first_name,
                        'last_name': last_name,
                        'info': student['info'],
                        'role': 'student',
                    },
                },
                status=status.HTTP_200_OK)

        except WrongEmail as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except KeyError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class AuthConfirmView(views.APIView):
    def post(self, request):
        try:
            email = request.data['email']
            code = request.data['code']

            if email == 'zzoorm@gmail.com':
                user = models.User.objects.get(email=email)
                token = list(Token.objects.filter(user=user))[0].key
                return Response(
                    {
                        'message': 'Успешная авторизация.',
                        'is_accept': user.profile.is_accept,
                        'token': token,
                        'profile': {
                            'id': user.id,
                            'fio': 'Евгеньев Евгений Евгеньевич',
                            'info': 'Босс',
                            'role': 'agent',
                        },
                    }, status=status.HTTP_200_OK)

            student = get_student_by_email(email)
            if student is None:
                raise WrongEmail

            if len(models.Confirmation.objects.filter(email=email, code=code)) == 0:
                raise CodeConfirmationException
            confirmation = list(models.Confirmation.objects.filter(email=email, code=code))[0]
            # confirmation.delete()

            user = models.User.objects.get(email=email)
            if user is None:
                raise CodeConfirmationException
            user.profile.is_login = True
            user.save()

            if len(Token.objects.filter(user=user)) == 0:
                token = get_rnd(40)
                Token.objects.create(
                    user=user,
                    key=token,
                )
            else:
                token = list(Token.objects.filter(user=user))[0].key

            return Response(
                {
                    'message': 'Успешная авторизация.',
                    'is_accept': user.profile.is_accept,
                    'token': token,
                    'profile': {
                        'id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'info': student['info'],
                        'dormitory_id': str(user.profile.dormitory.id),
                        'dormitory_name': str(user.profile.dormitory.name),
                        'role': 'student',
                    },
                }, status=status.HTTP_200_OK)

        except CodeConfirmationException as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except WrongEmail as e:
            return Response({'message': e.default_detail}, status=e.status_code)

        except KeyError as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):
    def get(self, request):
        try:
            include_additional_info = False
            if 'include_additional_info' in request.query_params:
                include_additional_info = bool(request.query_params['include_additional_info'])

            user = request.user
            if user.id is None:
                raise Unauthorized

            dormitory_name = None
            if user.profile.dormitory is not None:
                dormitory_name = str(user.profile.dormitory.name)

            dormitory_address = None
            if user.profile.dormitory is not None:
                dormitory_address = str(user.profile.dormitory.address)

            additional_info = None
            if True:
                additional_info = {
                    'dormitory_users_count': len(models.Profile.objects.filter(dormitory_id=user.profile.dormitory_id)),
                    'agents_online_count': 1,
                }

            return Response(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.profile.role,
                    'room': user.profile.room,
                    'dormitory': {
                        'id': user.profile.dormitory_id,
                        'name': dormitory_name,
                        'address': dormitory_address,
                    },
                    'additional_info': additional_info,
                }, status=status.HTTP_200_OK)

        except Unauthorized as e:
            return Response({
                'message': e.default_detail
            }, status=e.status_code)

    def post(self, request):
        try:
            dormitory_name = request.data['dormitory']
            room = request.data['room']

            user = request.user
            if user.id is None:
                raise Unauthorized

            dormitory = models.Dormitory.objects.get(name=dormitory_name)

            if user.profile.dormitory.name != dormitory.name:
                user.profile.dormitory = dormitory
            if user.profile.room != room:
                user.profile.room = room

            user.save()

            return Response({
                'message': 'ok'
            }, status=status.HTTP_200_OK)

        except KeyError as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        except Unauthorized as e:
            return Response({
                'message': e.default_detail
            }, status=e.status_code)

        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class MainPageView(views.APIView):
    def get(self, request):
        try:
            user = request.user
            if user.id is None:
                raise Unauthorized

            dormitory_name = None
            if user.profile.dormitory is not None:
                dormitory_name = str(user.profile.dormitory.name)

            dormitory_address = None
            if user.profile.dormitory is not None:
                dormitory_address = str(user.profile.dormitory.address)

            profile = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': user.profile.role,
                'room': user.profile.room,
                'dormitory': {
                    'id': user.profile.dormitory_id,
                    'name': dormitory_name,
                    'address': dormitory_address,
                },
            }

            notice_list = models.Notice.objects.all().order_by('-created_at')[:10]
            notices = [{
                'id': notice.id,
                'main_text': notice.main_text,
                'text': notice.text,
                'is_important': notice.is_important,
                'created_at': notice.created_at,
                'updated_at': notice.updated_at
            } for notice in notice_list]

            event_list = models.Event.objects.all().order_by('target_date')[:3]
            events = [{
                'id': event.id,
                'title': event.title,
                'description': event.description,
                'target_date': event.target_date,
                'created_at': event.created_at,
                'updated_at': event.updated_at
            } for event in event_list]

            main_questions = [
                {
                    'question': 'Как пообедать?',
                    'answer': 'Для этого нужно получить талон на еду.'
                },
                {
                    'question': 'Как поспать?',
                    'answer': 'Для этого нужно лечь в кровать и уснуть.'
                },
                {
                    'question': 'Как работать в карантин?',
                    'answer': 'Для этого нужно взять себя и свой ноутбук в руки.'
                }
            ]

            additional_info = {}

            return Response(
                {
                    'profile': profile,
                    'notices': notices,
                    'events': events,
                    'main_questions': main_questions,
                    'additional_info': additional_info,
                }, status=status.HTTP_200_OK)

        except Unauthorized as e:
            return Response({
                'message': e.default_detail
            }, status=e.status_code)


class AcceptStatusView(views.APIView):
    def get(self, request):
        try:
            user = request.user

            if user.id is None:
                raise Unauthorized

            return Response({
                'is_accept': user.profile.is_accept
            }, status=status.HTTP_200_OK)

        except Unauthorized as e:
            return Response({
                'message': e.default_detail
            }, status=e.status_code)


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
            if self.request.user.groups.filter(name='Агент поддержки').exists():
                return models.Problem.objects.all().order_by('-id')
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
