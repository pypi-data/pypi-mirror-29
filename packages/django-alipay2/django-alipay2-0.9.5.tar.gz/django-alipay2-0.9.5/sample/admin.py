from django.contrib import admin

from alipay.admin import AlipayPaymentAdmin
from alipay.models import AlipayPayment

admin.site.register(AlipayPayment, AlipayPaymentAdmin)
