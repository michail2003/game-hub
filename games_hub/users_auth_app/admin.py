from django.contrib import admin
from users_auth_app.models import CustomUser, Order,Voucher
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Order)


class VoucherAdmin(admin.ModelAdmin):
    list_display = ('code', 'gift_code', 'discount', 'user', 'created_at', 'expiration_date', 'usage_limit', 'used_count')
    list_filter = ('created_at',)  # ✅ Enables filtering by date in admin
    readonly_fields = ('gift_code', 'used_count', 'created_at')  # Prevent manual changes
    actions = ['delete_selected']  # Default action for bulk delete
admin.site.register(Voucher, VoucherAdmin)
