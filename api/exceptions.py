from rest_framework.exceptions import APIException


class Unauthorized(APIException):
    status_code = 401
    default_detail = 'Для просмотра этой страницы требуется авторизация.'
    default_code = 'unauthorized'
