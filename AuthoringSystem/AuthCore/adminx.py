#!/usr/bin/env python
# encoding: utf-8
import xadmin
from xadmin import views
from .models import UserModel, OrderInfo


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "授权系统后台"
    site_footer = "authoringsystem"


class UserModelAdmin(object):
    list_display = ['u_name', 'token', 'pubkey', 'privkey']
    list_filter = ['u_name']


class OrderInfoAdmin(object):
    list_display = ['order_user', 'product_name', 'total_num', 'consume_num', 'residue_num']
    list_filter = ['order_user']


xadmin.site.register(UserModel, UserModelAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)