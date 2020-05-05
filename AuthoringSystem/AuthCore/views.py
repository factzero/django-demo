# -*- coding: utf-8 -*-
import uuid
from django.core.cache import cache
from django.db.models import F
from rest_framework import status, exceptions, viewsets
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.response import Response
from AuthCore.models import UserModel, OrderInfo
from AuthCore.serializers import UserSerializer, OrderInfoSerializer
from AuthCore.constants import HTTP_ACTION_LOGIN
from AuthCore.auth import UserAuth, LicenseAuth, LicenseTokenAuth
from AuthCore.permissions import IsSuperUser
from AuthCore.crypto import rsa_gen_key, rsa_digital_sign_pkcs1, rsa_gen_key_pkcs1


class UsersAPIView(ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()
    authentication_classes = (UserAuth,)
    permission_classes = (IsSuperUser,)

    def post(self, request, *args, **kwargs):
        action = request.query_params.get('action')

        if HTTP_ACTION_LOGIN == action:
            u_name = request.data.get('u_name')
            u_password = request.data.get('u_password')
            try:
                user = UserModel.objects.get(u_name=u_name)
                if user.u_password == u_password:
                    token = uuid.uuid4().hex
                    cache.set(token, user.id)
                    pubkey, privkey = rsa_gen_key()
                    pubkey = pubkey.save_pkcs1().decode()
                    privkey = privkey.save_pkcs1().decode()
                    user.token = token
                    user.pubkey = pubkey
                    user.privkey = privkey
                    user.save()
                    data = {
                        'msg': 'login success',
                        'status': 200,
                        'token': token,
                        'pubkey': pubkey
                    }
                    return Response(data)
                else:
                    raise exceptions.AuthenticationFailed
            except UserModel.DoesNotExist:
                raise exceptions.NotFound
        else:
            raise exceptions.ValidationError


class LicenseAPIView(ListCreateAPIView):
    serializer_class = OrderInfoSerializer
    queryset = OrderInfo.objects.all()
    authentication_classes = (LicenseAuth,)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_name = request.data.get('productName')
        hardware_info = request.data.get('hardwareInfo')
        try:
            order = user.order_list.filter(product_name=product_name).first()
            if order is None:
                data = {
                    'msg': 'no product name',
                    'status': 201,
                }
                return Response(data)

            total_num = order.total_num
            consume_num = order.consume_num
            if consume_num >= total_num:
                print('no license residue')
                data = {
                    'msg': 'license failed',
                    'status': 201,
                }
            else:
                order.consume_num = F('consume_num') + 1
                order.residue_num = total_num - F('consume_num')
                order.save()

                # 数字签名
                license_info = product_name + hardware_info + str(order.consume_num)
                digital_sign = rsa_digital_sign_pkcs1(license_info, user.privkey)

                data = {
                    'msg': 'login success',
                    'status': 200,
                    'licenseInfo': license_info,
                    'digitalSign': digital_sign
                }
            return Response(data)
        except OrderInfo.DoesNotExist:
            raise exceptions.NotFound

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(order_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class V1AuthLoginAPIView(APIView):

    def post(self, request, *args, **kwargs):
        u_name = request.data.get('u_name')
        u_password = request.data.get('u_password')
        print(u_name, u_password)
        user = UserModel.objects.filter(u_name=u_name, u_password=u_password).first()
        expire_time = 60 * 60 * 2
        if user:
            token = uuid.uuid4().hex
            cache.set(token, user.id, timeout=expire_time)
            pubkey, privkey = rsa_gen_key_pkcs1()
            user.token = token
            user.pubkey = pubkey
            user.privkey = privkey
            user.save()
            data = {
                "status": 200,
                "msg": "登入成功",
                "results": {
                    "token": token,
                    "token_expire_time": expire_time,
                    "pubkey": pubkey
                }
            }
        else:
            data = {
                "status": 404,
                "msg": "用户名或密码错误"
            }
        return Response(data)


class V1GenLicenseAPIView(APIView):
    authentication_classes = (LicenseTokenAuth,)

    def post(self, request, *args, **kwargs):
        user = request.user
        product_name = request.data.get('product_name')
        hardware_info = request.data.get('hardware_info')
        order = user.order_list.filter(product_name=product_name).first()
        if order:
            total_num = order.total_num
            consume_num = order.consume_num
            if consume_num >= total_num:
                data = {
                    "status": 201,
                    "msg": product_name + "的license数量已消耗完"
                }
            else:
                order.consume_num = F('consume_num') + 1
                order.residue_num = total_num - F('consume_num')
                order.save()

                # 数字签名
                license_info = product_name + hardware_info + str(order.consume_num)
                digital_sign = rsa_digital_sign_pkcs1(license_info, user.privkey)
                data = {
                    "status": 200,
                    "msg": "license申请成功",
                    "results": {
                        'licenseInfo': license_info,
                        'digitalSign': digital_sign
                    }
                }
        else:
            data = {
                "status": 404,
                "msg": str(product_name) + "没有购买或者该产品不存在"
            }
        return Response(data)


class V1GetOrderInfoAPIView(ListAPIView):
    serializer_class = OrderInfoSerializer
    queryset = OrderInfo.objects.all()
    authentication_classes = (LicenseTokenAuth,)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(order_user=request.user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        results = []
        for res in serializer.data:
            print(res)
            results.append({
                "product_name": res.get("product_name"),
                "total_num": res.get("total_num"),
                "consume_num": res.get("consume_num"),
                "residue_num": res.get("residue_num")
            })
        data = {
            "status": 200,
            "msg": "订单查询成功",
            "results": results
        }
        return Response(data)


class V1TokenOvertimeAPIView(APIView):
    authentication_classes = (LicenseTokenAuth, )

    def post(self, request, *args, **kwargs):
        expire_time = 60 * 60 * 2
        token = request.data.get('token')
        cache.expire(token, timeout=expire_time)
        data = {
            "status": 200,
            "msg": "token过期时间已刷新",
            "results": {
                "token_expire_time": expire_time
            }
        }
        return Response(data)