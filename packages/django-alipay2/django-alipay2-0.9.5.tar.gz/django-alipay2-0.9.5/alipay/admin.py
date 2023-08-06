from django.contrib import admin


class AlipayPaymentAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'out_no', 'no', 'reference_id', 'subject',
                    'amount_total', 'buyer_email', 'status', 'is_succeed')
    search_fields = ('out_no', 'no', 'buyer_email', 'reference_id')
    list_filter = ('status',)
    raw_id_fields = ('user',)
