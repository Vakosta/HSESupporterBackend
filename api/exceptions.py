from rest_framework import status
from rest_framework.exceptions import APIException


class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Для просмотра этой страницы требуется авторизация.'
    default_code = 'unauthorized'


class WrongEmail(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Этот Email не принадлежит ни одному студенту/работнику.'


class CodeConfirmationException(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Неверный код подтверждения.'
