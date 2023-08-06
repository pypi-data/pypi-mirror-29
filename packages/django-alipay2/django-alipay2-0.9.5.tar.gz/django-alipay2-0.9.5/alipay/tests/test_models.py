from unittest.mock import Mock

from django.test import TestCase

from alipay.models import AlipayPayment
from alipay.signals import payment_succeed


class AlipayPaymentTest(TestCase):
    def test_signal_payment_succeed(self):
        payment = AlipayPayment.objects.create(
            out_no='123',
            subject='充值',
            body='1年365元',
            amount_total=0.01,
        )

        mock = Mock()
        payment_succeed.connect(mock)

        payment.status = AlipayPayment.TRADE_SUCCESS
        payment.save()
        self.assertEqual(mock.call_count, 1)

        payment.status = AlipayPayment.TRADE_FINISHED
        payment.save()
        self.assertEqual(mock.call_count, 1, '只有从未成功切换成成功的时候才抛signal')
