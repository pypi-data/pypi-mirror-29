from django.conf.urls import url

from alipay.views import AlipayCallbackView, AlipayRedirectView

urlpatterns = [
    url('^redirect/(?P<out_no>.*?)/$', AlipayRedirectView.as_view(), name='alipay_redirect'),
    url('^callback/$', AlipayCallbackView.as_view(), name='alipay_callback'),
]
