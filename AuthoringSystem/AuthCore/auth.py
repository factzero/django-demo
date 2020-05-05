from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from AuthCore.models import UserModel


class UserAuth(BaseAuthentication):

    def authenticate(self, request):
        if request.method == "GET":
            token = request.query_params.get('token')
            try:
                u_id = cache.get(token)
                user = UserModel.objects.get(pk=u_id)
                # print('UserAuth:{}, token:{}'.format(user.u_name, token))
                return user, token
            except UserModel.DoesNotExist:
                raise exceptions.AuthenticationFailed('No such user')


class LicenseAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.query_params.get('token')
        try:
            u_id = cache.get(token)
            user = UserModel.objects.get(pk=u_id)
            # print('LicenseAuth:{}, token:{}'.format(user.u_name, token))
            return user, token
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')


class LicenseTokenAuth(BaseAuthentication):

    def authenticate(self, request):
        token = request.data.get('token')
        try:
            u_id = cache.get(token)
            user = UserModel.objects.get(pk=u_id)
            # print('LicenseAuth:{}, token:{}'.format(user.u_name, token))
            return user, token
        except UserModel.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败，token错误')
