from django.db import models


class UserModel(models.Model):
    u_name = models.CharField(max_length=64, unique=True, verbose_name='�û���')
    u_password = models.CharField(max_length=256, verbose_name='����')
    is_super = models.BooleanField(default=False, verbose_name='�����û�')
    token = models.CharField(max_length=128, verbose_name='����')
    pubkey = models.CharField(max_length=512, default='', verbose_name='��Կ')
    privkey = models.CharField(max_length=1024, default='', verbose_name='��Կ')

    class Meta:
        verbose_name = "�û�"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.u_name


class OrderInfo(models.Model):
    product_name = models.CharField(max_length=64, verbose_name='��Ʒ��')
    total_num = models.IntegerField(default=0, verbose_name='�������Ȩ����')
    consume_num = models.IntegerField(default=0, verbose_name='���ĵ���Ȩ��')
    residue_num = models.IntegerField(default=0, verbose_name='ʣ�����Ȩ��')
    order_user = models.ForeignKey(UserModel, related_name='order_list', on_delete=models.CASCADE,
                                   null=True, blank=True, verbose_name='�û���Ϣ')

    class Meta:
        verbose_name = "��Ȩ����Ϣ"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_user.u_name
