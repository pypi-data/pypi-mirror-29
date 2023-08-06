"""
原则上需要定义两个view name：
    - alipay_redirect
    - alipay_callback

Example urlpatterns
-------------------

urlpatterns = [
        url('^redirect/(?P<pk>.*?)/$', AlipayRedirectView.as_view(), name='alipay_redirect'),
        url('^callback/$', AlipayCallbackView.as_view(), name='alipay_callback'),
    ]
"""

from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from alipay.alipay import AlipayClient
from alipay.models import AlipayPayment


def _get_api():
    conf = settings.ALIPAY
    if conf['sandbox']:
        return AlipayClient(
            pid='2088101122136241',
            key='760bdzec6y9goq7ctyx96ezkz78287de',
            seller='overseas_kgtest@163.com',
            gateway='https://openapi.alipaydev.com/gateway.do?',
        )
    else:
        return AlipayClient(
            pid=conf['pid'],
            key=conf['key'],
            seller=conf['seller'],
            gateway=conf['gateway'],
        )


class AlipayRedirectView(View):
    """
    他人生成AlipayPayment以后，跳转到本view就能重定向到alipay，继续完成支付流程
    样例见： example_alipay_create_view
    """

    def get_callback_url(self):
        """ 定义从alipay支付成功以后返回的URL，按需定义 """
        return settings.ALIPAY['SERVER_URL'] + reverse('alipay_callback')

    def handle_redirect(self, redirect_url):
        """ 得到alipay支付地址以后，定义如何跳转（默认为直接跳转，可以自己改成打开loading页面，用JS跳转 """
        return redirect(redirect_url)

    def get(self, request, out_no):
        payment = get_object_or_404(AlipayPayment, out_no=out_no)
        if payment.seller_email:
            assert payment.seller_email == settings.ALIPAY['seller']
        else:
            payment.seller_email = settings.ALIPAY['seller']
            payment.save()

        pay_url = _get_api().create_direct_pay_url(
            payment.out_no,
            payment.subject,
            payment.body,
            "{:.2f}".format(payment.amount_total),
            notify_url=self.get_callback_url(),
            return_url=self.get_callback_url(),
        )
        return self.handle_redirect(pay_url)


@method_decorator(csrf_exempt, name='dispatch')
class AlipayCallbackView(View):
    """
    从alipay支付成功以后，回来的页面，
    页面自己会处理payment成功的逻辑，成功以后会发送 payment_succeed signal
    业务逻辑只需要connect payment_succeed，然后做相应的处理即可
    """

    template_name = 'alipay/return.html'

    def payment_succeed(self, payment):
        """ 支付成功以后的返回结果，按需定义 """
        return render(self.request, self.template_name, context=dict(payment=payment))

    def payment_failed(self, payment, errors):
        """ 执行支付失败后的返回结果，按需定义 """
        print("handle_payment_execute_error", payment, errors)
        return HttpResponseServerError()

    def get(self, request):
        payment = self.handle_alipay_callback(request.GET)
        return self.payment_succeed(payment)

    def post(self, request):
        if self.handle_alipay_callback(request.POST):
            return HttpResponse("success")
        else:
            return HttpResponse("failed")

    @classmethod
    def handle_alipay_callback(cls, data):
        result = None
        try:
            result = _get_api().get_verified_result(data)
            assert result.is_success != 'F', 'payment failed'

            payment = AlipayPayment.objects.get(out_no=result.out_trade_no)

            # status 有推进才会接着处理
            if payment.status_weight(result.trade_status) > payment.status_weight(payment.status):
                payment.buyer_email = result.buyer_email
                payment.no = result.trade_no
                payment.status = result.trade_status
                payment.save()
            return payment

        except Exception as e:
            print("trade failed error=%s data=%s result=%s ", e, data, result)
            return None
