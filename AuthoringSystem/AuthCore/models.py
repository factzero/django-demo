from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=64, unique=True, verbose_name='用户名')
    u_password = models.CharField(max_length=256, verbose_name='密码')
    is_super = models.BooleanField(default=False, verbose_name='超级用户')
    token = models.CharField(max_length=128, verbose_name='令牌')
    pubkey = models.CharField(max_length=512, default='', verbose_name='公钥')
    privkey = models.CharField(max_length=1024, default='', verbose_name='密钥')

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.u_name


class OrderInfo(models.Model):
    product_name = models.CharField(max_length=64, verbose_name='产品名')
    total_num = models.IntegerField(default=0, verbose_name='购买的授权总数')
    consume_num = models.IntegerField(default=0, verbose_name='消耗的授权数')
    residue_num = models.IntegerField(default=0, verbose_name='剩余的授权数')
    order_user = models.ForeignKey(UserModel, related_name='order_list', on_delete=models.CASCADE,
                                   null=True, blank=True, verbose_name='用户信息')

    class Meta:
        verbose_name = "授权数信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_user.u_name
