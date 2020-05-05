from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=64, unique=True)
    u_password = models.CharField(max_length=256)
    is_super = models.BooleanField(default=False)
    token = models.CharField(max_length=128)
    pubkey = models.CharField(max_length=512, default='')
    privkey = models.CharField(max_length=1024, default='')


class OrderInfo(models.Model):
    product_name = models.CharField(max_length=64)
    total_num = models.IntegerField(default=0)
    consume_num = models.IntegerField(default=0)
    residue_num = models.IntegerField(default=0)
    order_user = models.ForeignKey(UserModel, related_name='order_list', on_delete=models.CASCADE, null=True, blank=True)