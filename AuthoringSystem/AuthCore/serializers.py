from rest_framework import serializers
from AuthCore.models import UserModel, OrderInfo


class OrderInfoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderInfo
        fields = ('id', 'product_name', 'total_num', 'consume_num', 'residue_num')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    order_list = OrderInfoSerializer(many=True, read_only=True)

    class Meta:
        model = UserModel
        fields = ('url', 'id', 'u_name', 'u_password', 'order_list')
