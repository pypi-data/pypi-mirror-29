from django.test import RequestFactory, TestCase

from alipay.models import AlipayPayment
from alipay.views import AlipayRedirectView


class AlipayRedirectViewTest(TestCase):
    def test_create(self):
        payment = AlipayPayment.objects.create(
            out_no='123',
            subject='充值',
            body='1年365元',
            amount_total=0.01,
        )

        view = AlipayRedirectView.as_view()
        factory = RequestFactory()
        req = factory.get('/')

        resp = view(req, out_no=payment.out_no)
        self.assertTrue('alipay' in resp.url, '跳转到alipay')
