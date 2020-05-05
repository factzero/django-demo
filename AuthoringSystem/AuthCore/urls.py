from django.conf.urls import url
from AuthCore import views


urlpatterns = [
    url(r'^users/$', views.UsersAPIView.as_view()),
    url(r'^users/(?P<pk>\d+)/$', views.UsersAPIView.as_view(), name='usermodel-detail'),
    url(r'^license/$', views.LicenseAPIView.as_view()),
    url(r'^license/(?P<pk>\d+)/$', views.LicenseAPIView.as_view(), name='orderinfo-detail'),
    url(r'^v1/login/$', views.V1AuthLoginAPIView.as_view()),
    url(r'^v1/license/$', views.V1GenLicenseAPIView.as_view()),
    url(r'^v1/orderinfo/$', views.V1GetOrderInfoAPIView.as_view()),
    url(r'^v1/token-overtime/$', views.V1TokenOvertimeAPIView.as_view()),
]